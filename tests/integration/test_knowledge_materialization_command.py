"""Integration tests for runtime knowledge content materialization."""

from __future__ import annotations

import hashlib
import io
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.knowledge.models import (
    Category,
    IndexingStatus,
    KnowledgeChunk,
    KnowledgeDocument,
    Language,
)
from apps.knowledge.services import content_manifest

MANIFEST_PATH = Path("backend/apps/knowledge/data/knowledge_content_v1.json")
BASELINE_PATH = Path("docs/knowledge/KNOWLEDGE-CONTENT-BASELINE-001.md")


class ManifestDocumentDict(TypedDict):
    concept_id: str
    title: str
    slug: str
    language: str
    category: str
    content: str
    is_active: bool


class ManifestDict(TypedDict):
    baseline: str
    version: str
    expected_documents: int
    documents: list[ManifestDocumentDict]


def _load_manifest_dict() -> ManifestDict:
    raw_manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert isinstance(raw_manifest, dict)
    baseline = raw_manifest.get("baseline")
    version = raw_manifest.get("version")
    expected_documents = raw_manifest.get("expected_documents")
    raw_documents = raw_manifest.get("documents")

    assert isinstance(baseline, str)
    assert isinstance(version, str)
    assert isinstance(expected_documents, int)
    assert isinstance(raw_documents, list)

    documents: list[ManifestDocumentDict] = []
    for raw_document in raw_documents:
        assert isinstance(raw_document, dict)

        concept_id = raw_document.get("concept_id")
        title = raw_document.get("title")
        slug = raw_document.get("slug")
        language = raw_document.get("language")
        category = raw_document.get("category")
        content = raw_document.get("content")
        is_active = raw_document.get("is_active")

        assert isinstance(concept_id, str)
        assert isinstance(title, str)
        assert isinstance(slug, str)
        assert isinstance(language, str)
        assert isinstance(category, str)
        assert isinstance(content, str)
        assert isinstance(is_active, bool)

        documents.append(
            {
                "concept_id": concept_id,
                "title": title,
                "slug": slug,
                "language": language,
                "category": category,
                "content": content,
                "is_active": is_active,
            }
        )

    return {
        "baseline": baseline,
        "version": version,
        "expected_documents": expected_documents,
        "documents": documents,
    }


def _parse_editorial_baseline() -> list[ManifestDocumentDict]:
    text = BASELINE_PATH.read_text(encoding="utf-8")
    sections = re.split(r"(?=^### KB-)", text, flags=re.M)
    documents: list[ManifestDocumentDict] = []

    for section in sections:
        if not section.startswith("### KB-"):
            continue

        heading_match = re.match(r"^### (KB-[A-Z]+-\d+) — ", section)
        assert heading_match is not None
        concept_id = heading_match.group(1).removeprefix("KB-")

        metadata_block = re.search(
            r"^#### Metadata\n\n(.*?)\n#### PT-BR\n",
            section,
            flags=re.S | re.M,
        )
        assert metadata_block is not None
        category_match = re.search(r"^Category: (.+)$", metadata_block.group(1), flags=re.M)
        assert category_match is not None
        category = category_match.group(1).strip()

        for language_heading, expected_language, next_heading in [
            ("PT-BR", "pt-br", "#### EN"),
            ("EN", "en", "#### Evidence / Maturity Notes"),
        ]:
            pattern = (
                rf"^#### {re.escape(language_heading)}\n\n(.*?)\n"
                rf"##### Approved Content\n\n(.*?)(?=\n{re.escape(next_heading)}\n)"
            )
            block_match = re.search(
                pattern,
                section,
                flags=re.S | re.M,
            )
            assert block_match is not None
            header_block = block_match.group(1)
            title_match = re.search(r"^Title: (.+)$", header_block, flags=re.M)
            slug_match = re.search(r"^Slug: (.+)$", header_block, flags=re.M)
            language_match = re.search(r"^Language: (.+)$", header_block, flags=re.M)
            assert title_match is not None
            assert slug_match is not None
            assert language_match is not None

            documents.append(
                {
                    "concept_id": concept_id,
                    "title": title_match.group(1).strip(),
                    "slug": slug_match.group(1).strip(),
                    "language": language_match.group(1).strip(),
                    "category": category,
                    "content": block_match.group(2).rstrip("\n"),
                    "is_active": True,
                }
            )
            assert documents[-1]["language"] == expected_language

    return documents


def _write_manifest(path: Path, manifest: ManifestDict) -> None:
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class TestKnowledgeRuntimeManifest:
    """AC-RM-01 through AC-RM-04 and AC-RM-18 manifest integrity coverage."""

    def test_manifest_matches_editorial_baseline(self) -> None:
        manifest = _load_manifest_dict()
        documents = manifest["documents"]

        assert manifest["baseline"] == "KNOWLEDGE-CONTENT-BASELINE-001"
        assert manifest["version"] == "1.0"
        assert manifest["expected_documents"] == 58
        assert len(documents) == 58
        assert len({document["concept_id"] for document in documents}) == 29
        assert sum(document["language"] == "pt-br" for document in documents) == 29
        assert sum(document["language"] == "en" for document in documents) == 29
        assert {document["language"] for document in documents} == {"pt-br", "en"}
        assert {document["category"] for document in documents} == {
            "PROFILE",
            "EXPERIENCE",
            "SKILL",
            "PROJECT",
            "ENGINEERING",
            "PROCESS",
            "PORTFOLIO",
            "GENERAL",
        }
        assert documents == _parse_editorial_baseline()

        digest_source = json.dumps(documents, ensure_ascii=False, sort_keys=True).encode("utf-8")
        assert hashlib.sha256(digest_source).hexdigest() == (
            "8faf70e903117c4e1e00b054f0af1e57dc47db3f1deec20b75c8c48934c85b36"
        )


@pytest.mark.django_db
class TestMaterializeKnowledgeCommand:
    """Command behavior for dry runs, materialization, and managed-row reconciliation."""

    def test_materializes_complete_corpus_from_empty_state(self, monkeypatch) -> None:
        indexing_called = False

        def fail_if_indexed(*args, **kwargs):
            nonlocal indexing_called
            indexing_called = True
            raise AssertionError("IndexingService must not be used during materialization.")

        monkeypatch.setattr(
            "apps.knowledge.services.indexing.IndexingService.index_document",
            fail_if_indexed,
        )

        out = io.StringIO()
        call_command("materialize_knowledge", stdout=out)

        assert not indexing_called
        assert KnowledgeDocument.objects.count() == 58
        assert KnowledgeChunk.objects.count() == 0
        assert KnowledgeDocument.objects.filter(language=Language.PT_BR).count() == 29
        assert KnowledgeDocument.objects.filter(language=Language.EN).count() == 29
        document = KnowledgeDocument.objects.get(slug="professional-profile-en")
        assert document.indexing_status == IndexingStatus.PENDING
        assert document.embedding_model == ""
        assert document.indexed_at is None
        assert document.last_index_error == ""
        assert document.index_version == 1
        assert "Baseline: KNOWLEDGE-CONTENT-BASELINE-001" in out.getvalue()
        assert "Validated documents: 58" in out.getvalue()
        assert "Created: 58" in out.getvalue()
        assert "Updated: 0" in out.getvalue()
        assert "Unchanged: 0" in out.getvalue()

    def test_second_execution_is_idempotent_and_does_not_resave_rows(self) -> None:
        call_command("materialize_knowledge")
        before = {
            document.slug: document.updated_at
            for document in KnowledgeDocument.objects.order_by("slug")
        }

        out = io.StringIO()
        call_command("materialize_knowledge", stdout=out)

        after = {
            document.slug: document.updated_at
            for document in KnowledgeDocument.objects.order_by("slug")
        }
        assert before == after
        assert "Created: 0" in out.getvalue()
        assert "Updated: 0" in out.getvalue()
        assert "Unchanged: 58" in out.getvalue()

    def test_dry_run_performs_zero_database_writes(self) -> None:
        out = io.StringIO()
        call_command("materialize_knowledge", "--dry-run", stdout=out)

        assert KnowledgeDocument.objects.count() == 0
        assert KnowledgeChunk.objects.count() == 0
        assert "Baseline: KNOWLEDGE-CONTENT-BASELINE-001" in out.getvalue()
        assert "Validated documents: 58" in out.getvalue()
        assert "Would create: 58" in out.getvalue()
        assert "Would update: 0" in out.getvalue()
        assert "Would leave unchanged: 0" in out.getvalue()
        assert "Dry run complete. No database changes performed." in out.getvalue()

    def test_invalid_manifest_fails_before_persistence(self, monkeypatch, tmp_path: Path) -> None:
        manifest = _load_manifest_dict()
        manifest["expected_documents"] = 57
        path = tmp_path / "invalid_manifest.json"
        _write_manifest(path, manifest)

        monkeypatch.setattr(content_manifest, "MANIFEST_PATH", path)

        with pytest.raises(CommandError):
            call_command("materialize_knowledge")

        assert KnowledgeDocument.objects.count() == 0
        assert KnowledgeChunk.objects.count() == 0

    def test_partial_validation_failure_leaves_zero_partial_corpus_writes(
        self,
        monkeypatch,
        tmp_path: Path,
    ) -> None:
        manifest = _load_manifest_dict()
        manifest["documents"][10]["content"] = "   "
        path = tmp_path / "partial_failure_manifest.json"
        _write_manifest(path, manifest)

        monkeypatch.setattr(content_manifest, "MANIFEST_PATH", path)

        with pytest.raises(CommandError):
            call_command("materialize_knowledge")

        assert KnowledgeDocument.objects.count() == 0
        assert KnowledgeChunk.objects.count() == 0

    def test_existing_unmanaged_documents_remain_untouched(self) -> None:
        unmanaged = KnowledgeDocument.objects.create(
            title="Unmanaged Doc",
            slug="unmanaged-doc",
            language=Language.EN,
            category=Category.GENERAL,
            content="Manual content that must remain untouched.",
            is_active=False,
            indexing_status=IndexingStatus.INDEXED,
            embedding_model="text-embedding-3-small",
            indexed_at=datetime(2026, 9, 3, tzinfo=UTC),
            index_version=7,
        )
        original_updated_at = unmanaged.updated_at

        call_command("materialize_knowledge")
        unmanaged.refresh_from_db()

        assert KnowledgeDocument.objects.count() == 59
        assert unmanaged.title == "Unmanaged Doc"
        assert unmanaged.content == "Manual content that must remain untouched."
        assert unmanaged.is_active is False
        assert unmanaged.indexing_status == IndexingStatus.INDEXED
        assert unmanaged.embedding_model == "text-embedding-3-small"
        assert unmanaged.index_version == 7
        assert unmanaged.updated_at == original_updated_at

    def test_changed_managed_content_is_reconciled_and_preserves_existing_index_data(self) -> None:
        call_command("materialize_knowledge")
        document = KnowledgeDocument.objects.get(slug="professional-profile-en")
        authoritative_content = document.content
        document.content = "Drifted content."
        document.indexing_status = IndexingStatus.INDEXED
        document.embedding_model = "text-embedding-3-small"
        document.index_version = 9
        document.indexed_at = datetime(2026, 9, 3, tzinfo=UTC)
        document.save()
        chunk = KnowledgeChunk.objects.create(
            document=document,
            sequence=0,
            content="Existing chunk that must be preserved.",
            embedding=[0.0] * 1024,
        )

        call_command("materialize_knowledge")
        document.refresh_from_db()
        chunk.refresh_from_db()

        assert document.content == authoritative_content
        assert document.indexing_status == IndexingStatus.PENDING
        assert document.embedding_model == "text-embedding-3-small"
        assert document.index_version == 9
        assert document.indexed_at == datetime(2026, 9, 3, tzinfo=UTC)
        assert KnowledgeChunk.objects.filter(document=document).count() == 1
        assert chunk.content == "Existing chunk that must be preserved."

    def test_is_active_only_reconciliation_preserves_existing_index_artifacts(self) -> None:
        call_command("materialize_knowledge")
        document = KnowledgeDocument.objects.get(slug="professional-profile-en")
        document.is_active = False
        document.indexing_status = IndexingStatus.INDEXED
        document.embedding_model = "text-embedding-3-small"
        document.index_version = 4
        document.indexed_at = datetime(2026, 9, 3, tzinfo=UTC)
        document.save()
        KnowledgeChunk.objects.create(
            document=document,
            sequence=0,
            content="Existing chunk that must remain.",
            embedding=[0.0] * 1024,
        )

        call_command("materialize_knowledge")
        document.refresh_from_db()

        assert document.is_active is True
        assert document.indexing_status == IndexingStatus.INDEXED
        assert document.embedding_model == "text-embedding-3-small"
        assert document.index_version == 4
        assert document.indexed_at == datetime(2026, 9, 3, tzinfo=UTC)
        assert document.chunks.count() == 1

    def test_unsafe_language_or_category_drift_on_indexed_document_fails_closed(self) -> None:
        call_command("materialize_knowledge")
        document = KnowledgeDocument.objects.get(slug="professional-profile-en")
        document.language = Language.PT_BR
        document.category = Category.GENERAL
        document.indexing_status = IndexingStatus.INDEXED
        document.save()

        with pytest.raises(CommandError, match="Cannot reconcile indexed metadata drift"):
            call_command("materialize_knowledge")

        assert KnowledgeDocument.objects.count() == 58
        drifted = KnowledgeDocument.objects.get(slug="professional-profile-en")
        assert drifted.language == Language.PT_BR
        assert drifted.category == Category.GENERAL

    def test_unsafe_language_or_category_drift_on_pending_previously_indexed_document_fails_closed(
        self,
    ) -> None:
        call_command("materialize_knowledge")
        drifted = KnowledgeDocument.objects.get(slug="professional-profile-en")
        authoritative_content = drifted.content
        drifted.language = Language.PT_BR
        drifted.category = Category.GENERAL
        drifted.content = "Locally drifted content that should remain untouched after failure."
        drifted.indexing_status = IndexingStatus.PENDING
        drifted.embedding_model = "text-embedding-3-small"
        drifted.index_version = 9
        drifted.indexed_at = datetime(2026, 9, 3, tzinfo=UTC)
        drifted.last_index_error = "Previous successful index artifacts preserved."
        drifted.save()
        preserved_chunk = KnowledgeChunk.objects.create(
            document=drifted,
            sequence=0,
            content="Previously indexed chunk that must remain unchanged.",
            embedding=[0.0] * 1024,
        )

        other_managed = KnowledgeDocument.objects.get(slug="professional-profile-pt-br")
        original_other_content = other_managed.content
        other_managed.is_active = False
        other_managed.save()
        original_other_updated_at = other_managed.updated_at

        with pytest.raises(CommandError, match="Cannot reconcile indexed metadata drift"):
            call_command("materialize_knowledge")

        drifted.refresh_from_db()
        preserved_chunk.refresh_from_db()
        other_managed.refresh_from_db()

        assert drifted.language == Language.PT_BR
        assert drifted.category == Category.GENERAL
        assert (
            drifted.content == "Locally drifted content that should remain untouched after failure."
        )
        assert drifted.indexing_status == IndexingStatus.PENDING
        assert drifted.embedding_model == "text-embedding-3-small"
        assert drifted.index_version == 9
        assert drifted.indexed_at == datetime(2026, 9, 3, tzinfo=UTC)
        assert drifted.last_index_error == "Previous successful index artifacts preserved."
        assert drifted.chunks.count() == 1
        assert preserved_chunk.content == "Previously indexed chunk that must remain unchanged."

        assert other_managed.is_active is False
        assert other_managed.content == original_other_content
        assert other_managed.updated_at == original_other_updated_at
        assert authoritative_content != drifted.content

    def test_non_indexed_language_or_category_drift_can_be_reconciled(self) -> None:
        call_command("materialize_knowledge")
        document = KnowledgeDocument.objects.get(slug="professional-profile-en")
        document.language = Language.PT_BR
        document.category = Category.GENERAL
        document.indexing_status = IndexingStatus.PENDING
        document.save()

        call_command("materialize_knowledge")
        document.refresh_from_db()

        assert document.language == Language.EN
        assert document.category == Category.PROFILE
        assert document.indexing_status == IndexingStatus.PENDING
