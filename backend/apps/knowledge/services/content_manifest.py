"""Runtime manifest loading and validation for approved knowledge content."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypedDict

from django.core.exceptions import ValidationError
from django.db.models import Field

from apps.knowledge.models import KnowledgeDocument, Language

MANIFEST_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge_content_v1.json"
EXPECTED_BASELINE = "KNOWLEDGE-CONTENT-BASELINE-001"
EXPECTED_DOCUMENTS = 58
EXPECTED_CONCEPTS = 29
REQUIRED_DOCUMENT_FIELDS = {
    "concept_id",
    "title",
    "slug",
    "language",
    "category",
    "content",
    "is_active",
}
MANAGED_SOURCE_FIELDS = ("title", "language", "category", "content", "is_active")


class ManifestValidationError(ValueError):
    """Raised when the runtime manifest is structurally or semantically invalid."""


class RawManifestDocument(TypedDict):
    """Typed JSON representation of one manifest document entry."""

    concept_id: str
    title: str
    slug: str
    language: str
    category: str
    content: str
    is_active: bool


class RawKnowledgeContentManifest(TypedDict):
    """Typed JSON representation of the manifest file."""

    baseline: str
    version: str
    expected_documents: int
    documents: list[RawManifestDocument]


@dataclass(frozen=True)
class ManifestDocument:
    """Validated runtime representation of one KnowledgeDocument variant."""

    concept_id: str
    title: str
    slug: str
    language: str
    category: str
    content: str
    is_active: bool


@dataclass(frozen=True)
class KnowledgeContentManifest:
    """Validated runtime manifest metadata and document entries."""

    baseline: str
    version: str
    expected_documents: int
    documents: tuple[ManifestDocument, ...]


def load_knowledge_content_manifest(
    path: Path | None = None,
) -> KnowledgeContentManifest:
    """Load and fully validate the tracked runtime manifest."""

    manifest_path = path or MANIFEST_PATH

    try:
        raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestValidationError(f"Manifest file not found: {manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestValidationError(f"Manifest is not valid JSON: {exc}") from exc

    return validate_knowledge_content_manifest(raw_manifest)


def validate_knowledge_content_manifest(raw_manifest: Any) -> KnowledgeContentManifest:
    """Validate the entire manifest before any persistence occurs."""

    if not isinstance(raw_manifest, dict):
        raise ManifestValidationError("Manifest root must be a JSON object.")

    errors: list[str] = []
    baseline_value = raw_manifest.get("baseline")
    version_value = raw_manifest.get("version")
    expected_documents_value = raw_manifest.get("expected_documents")
    documents_value = raw_manifest.get("documents")

    baseline: str | None = None
    version: str | None = None
    expected_documents: int | None = None

    if baseline_value != EXPECTED_BASELINE:
        errors.append(f"Manifest baseline must be {EXPECTED_BASELINE!r}; got {baseline_value!r}.")
    elif isinstance(baseline_value, str):
        baseline = baseline_value

    if not isinstance(version_value, str) or not version_value.strip():
        errors.append("Manifest version must be a nonblank string.")
    else:
        version = version_value

    if expected_documents_value != EXPECTED_DOCUMENTS:
        errors.append(
            "Manifest expected_documents must be "
            f"{EXPECTED_DOCUMENTS}; got {expected_documents_value!r}."
        )
    elif isinstance(expected_documents_value, int):
        expected_documents = expected_documents_value

    if not isinstance(documents_value, list):
        errors.append("Manifest documents must be a list.")
        documents: list[Any] = []
    else:
        documents = documents_value

    validated_documents: list[ManifestDocument] = []
    seen_slugs: set[str] = set()
    language_counts: Counter[str] = Counter()
    concept_languages: defaultdict[str, Counter[str]] = defaultdict(Counter)

    for index, raw_document in enumerate(documents):
        validated_document = _validate_document(
            index=index,
            raw_document=raw_document,
            errors=errors,
        )
        if validated_document is None:
            continue

        validated_documents.append(validated_document)
        language_counts[validated_document.language] += 1
        concept_languages[validated_document.concept_id][validated_document.language] += 1

        if validated_document.slug in seen_slugs:
            errors.append(f"Duplicate slug detected: {validated_document.slug!r}.")
        seen_slugs.add(validated_document.slug)

    if len(validated_documents) != EXPECTED_DOCUMENTS:
        errors.append(
            f"Manifest must contain exactly {EXPECTED_DOCUMENTS} documents; "
            f"got {len(validated_documents)}."
        )
    if len(seen_slugs) != EXPECTED_DOCUMENTS:
        errors.append(
            f"Manifest must contain exactly {EXPECTED_DOCUMENTS} unique slugs; "
            f"got {len(seen_slugs)}."
        )
    if len(concept_languages) != EXPECTED_CONCEPTS:
        errors.append(
            f"Manifest must contain exactly {EXPECTED_CONCEPTS} unique concept IDs; "
            f"got {len(concept_languages)}."
        )
    if language_counts[Language.PT_BR] != EXPECTED_CONCEPTS:
        errors.append(
            f"Manifest must contain exactly {EXPECTED_CONCEPTS} pt-br documents; "
            f"got {language_counts[Language.PT_BR]}."
        )
    if language_counts[Language.EN] != EXPECTED_CONCEPTS:
        errors.append(
            f"Manifest must contain exactly {EXPECTED_CONCEPTS} en documents; "
            f"got {language_counts[Language.EN]}."
        )

    for concept_id, counts in sorted(concept_languages.items()):
        if counts[Language.PT_BR] != 1 or counts[Language.EN] != 1:
            errors.append(
                "Each concept must have exactly one pt-br and one en document; "
                f"{concept_id!r} has pt-br={counts[Language.PT_BR]}, en={counts[Language.EN]}."
            )

    if errors:
        raise ManifestValidationError("\n".join(errors))

    assert baseline is not None
    assert version is not None
    assert expected_documents is not None

    return KnowledgeContentManifest(
        baseline=baseline,
        version=version,
        expected_documents=expected_documents,
        documents=tuple(validated_documents),
    )


def _validate_document(
    *,
    index: int,
    raw_document: Any,
    errors: list[str],
) -> ManifestDocument | None:
    if not isinstance(raw_document, dict):
        errors.append(f"Document #{index + 1} must be an object.")
        return None

    raw_keys = set(raw_document)
    missing_fields = sorted(REQUIRED_DOCUMENT_FIELDS - raw_keys)
    unexpected_fields = sorted(raw_keys - REQUIRED_DOCUMENT_FIELDS)

    if missing_fields:
        errors.append(
            f"Document #{index + 1} is missing required fields: {', '.join(missing_fields)}."
        )
    if unexpected_fields:
        errors.append(
            f"Document #{index + 1} has unexpected fields: {', '.join(unexpected_fields)}."
        )
    if missing_fields:
        return None

    concept_id = raw_document["concept_id"]
    title = raw_document["title"]
    slug = raw_document["slug"]
    language = raw_document["language"]
    category = raw_document["category"]
    content = raw_document["content"]
    is_active = raw_document["is_active"]

    if not isinstance(concept_id, str) or not concept_id.strip():
        errors.append(f"Document #{index + 1} concept_id must be a nonblank string.")
    if not isinstance(title, str) or not title.strip():
        errors.append(f"Document #{index + 1} title must be a nonblank string.")
    if not isinstance(content, str) or not content.strip():
        errors.append(f"Document #{index + 1} content must be a nonblank string.")
    if not isinstance(is_active, bool):
        errors.append(f"Document #{index + 1} is_active must be a boolean.")

    _validate_model_field(field_name="slug", value=slug, index=index, errors=errors)
    _validate_model_field(field_name="language", value=language, index=index, errors=errors)
    _validate_model_field(field_name="category", value=category, index=index, errors=errors)

    return ManifestDocument(
        concept_id=concept_id,
        title=title,
        slug=slug,
        language=language,
        category=category,
        content=content,
        is_active=is_active,
    )


def _validate_model_field(
    *,
    field_name: str,
    value: Any,
    index: int,
    errors: list[str],
) -> None:
    field = KnowledgeDocument._meta.get_field(field_name)
    if not isinstance(field, Field):
        errors.append(f"Document #{index + 1} has invalid model field lookup: {field_name!r}.")
        return
    try:
        field.clean(value, None)
    except ValidationError as exc:
        errors.append(f"Document #{index + 1} has invalid {field_name!r}: {value!r} ({exc}).")
