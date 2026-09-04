"""Materialize the approved runtime knowledge manifest into KnowledgeDocument rows."""

from __future__ import annotations

from dataclasses import dataclass

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.knowledge.models import IndexingStatus, KnowledgeDocument
from apps.knowledge.services.content_manifest import (
    MANAGED_SOURCE_FIELDS,
    ManifestDocument,
    ManifestValidationError,
    load_knowledge_content_manifest,
)


@dataclass(frozen=True)
class PlannedOperation:
    """A fully preflighted reconciliation step for one manifest-owned slug."""

    action: str
    slug: str
    values: dict[str, object]
    update_fields: tuple[str, ...] = ()


class Command(BaseCommand):
    """Reconcile manifest-managed KnowledgeDocument rows by unique slug."""

    help = "Materialize the approved Knowledge Base runtime manifest"

    def _has_metadata_drift_unsafe_index_state(self, document: KnowledgeDocument) -> bool:
        """Return whether metadata drift must fail closed for this document."""
        return document.indexing_status == IndexingStatus.INDEXED or document.indexed_at is not None

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate and calculate materialization changes without writing to the database.",
        )

    def handle(self, *args, **options) -> None:
        dry_run = options["dry_run"]

        try:
            manifest = load_knowledge_content_manifest()
        except ManifestValidationError as exc:
            raise CommandError(str(exc)) from exc

        existing_documents = KnowledgeDocument.objects.in_bulk(
            [document.slug for document in manifest.documents],
            field_name="slug",
        )

        try:
            plan = self._build_reconciliation_plan(manifest.documents, existing_documents)
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        created = sum(1 for operation in plan if operation.action == "create")
        updated = sum(1 for operation in plan if operation.action == "update")
        unchanged = sum(1 for operation in plan if operation.action == "unchanged")

        self.stdout.write(f"Baseline: {manifest.baseline}")
        self.stdout.write(f"Validated documents: {len(manifest.documents)}")

        if dry_run:
            self.stdout.write(f"Would create: {created}")
            self.stdout.write(f"Would update: {updated}")
            self.stdout.write(f"Would leave unchanged: {unchanged}")
            self.stdout.write("Dry run complete. No database changes performed.")
            return

        with transaction.atomic():
            for operation in plan:
                if operation.action == "create":
                    KnowledgeDocument.objects.create(**operation.values)
                    continue

                if operation.action == "update":
                    document = existing_documents[operation.slug]
                    for field_name, value in operation.values.items():
                        setattr(document, field_name, value)
                    document.save(update_fields=[*operation.update_fields, "updated_at"])

        self.stdout.write(f"Created: {created}")
        self.stdout.write(f"Updated: {updated}")
        self.stdout.write(f"Unchanged: {unchanged}")

    def _build_reconciliation_plan(
        self,
        manifest_documents: tuple[ManifestDocument, ...],
        existing_documents: dict[str, KnowledgeDocument],
    ) -> list[PlannedOperation]:
        plan: list[PlannedOperation] = []
        preflight_errors: list[str] = []

        for document in manifest_documents:
            authoritative_values = {
                "title": document.title,
                "slug": document.slug,
                "language": document.language,
                "category": document.category,
                "content": document.content,
                "is_active": document.is_active,
            }
            existing = existing_documents.get(document.slug)
            if existing is None:
                plan.append(
                    PlannedOperation(
                        action="create",
                        slug=document.slug,
                        values=authoritative_values,
                    )
                )
                continue

            changed_fields = {
                field_name: authoritative_values[field_name]
                for field_name in MANAGED_SOURCE_FIELDS
                if getattr(existing, field_name) != authoritative_values[field_name]
            }
            if not changed_fields:
                plan.append(
                    PlannedOperation(
                        action="unchanged",
                        slug=document.slug,
                        values={},
                    )
                )
                continue

            unsafe_fields = {"language", "category"} & set(changed_fields)
            if unsafe_fields and self._has_metadata_drift_unsafe_index_state(existing):
                preflight_errors.append(
                    "Cannot reconcile indexed metadata drift for "
                    f"{document.slug!r}: {', '.join(sorted(unsafe_fields))}. "
                    "Reindex lifecycle does not provide a safe in-place metadata transition."
                )
                continue

            if "content" in changed_fields and existing.indexing_status != IndexingStatus.PENDING:
                changed_fields["indexing_status"] = IndexingStatus.PENDING

            plan.append(
                PlannedOperation(
                    action="update",
                    slug=document.slug,
                    values=changed_fields,
                    update_fields=tuple(changed_fields),
                )
            )

        if preflight_errors:
            raise ValueError("\n".join(preflight_errors))

        return plan
