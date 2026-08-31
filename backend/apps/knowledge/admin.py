"""Django Admin registration for the Knowledge application.

Governing documents: SPEC-004 §38–40.
"""

from __future__ import annotations

import logging

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.knowledge.integrations.openai_embedding_provider import OpenAIEmbeddingProvider
from apps.knowledge.models import IndexingStatus, KnowledgeChunk, KnowledgeDocument
from apps.knowledge.services.embedding_provider import EmbeddingError
from apps.knowledge.services.indexing import IndexingService

logger = logging.getLogger(__name__)


class KnowledgeChunkInline(admin.TabularInline):
    """Read-only diagnostic view of derived chunks."""

    model = KnowledgeChunk
    extra = 0
    fields = ("sequence", "content", "created_at")
    readonly_fields = ("sequence", "content", "created_at")
    can_delete = False
    show_change_link = False

    def has_add_permission(self, request, obj=None) -> bool:
        return False


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    """Administrative control for knowledge source documents."""

    list_display = (
        "title",
        "slug",
        "language",
        "category",
        "is_active",
        "indexing_status",
        "indexed_at",
    )
    list_filter = (
        "language",
        "category",
        "is_active",
        "indexing_status",
    )
    search_fields = ("title", "slug", "content")
    readonly_fields = (
        "indexing_status",
        "index_version",
        "embedding_model",
        "indexed_at",
        "last_index_error",
        "created_at",
        "updated_at",
    )
    inlines = [KnowledgeChunkInline]
    actions = ["reindex_selected_documents"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "language",
                    "category",
                    "content",
                    "is_active",
                ),
            },
        ),
        (
            _("Indexing metadata"),
            {
                "fields": (
                    "indexing_status",
                    "index_version",
                    "embedding_model",
                    "indexed_at",
                    "last_index_error",
                ),
            },
        ),
        (
            _("Audit"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change) -> None:
        """Mark content changes as requiring reindexing.

        Last successful index metadata (embedding_model, indexed_at) is preserved
        until a new successful index replaces it.
        """
        if change and "content" in form.changed_data:
            obj.indexing_status = IndexingStatus.PENDING
        super().save_model(request, obj, form, change)

    @admin.action(description=_("Reindex selected knowledge documents"))
    def reindex_selected_documents(self, request, queryset) -> None:
        """Trigger production indexing for selected documents."""
        try:
            provider = self._create_provider()
        except EmbeddingError as exc:
            logger.warning("Admin reindex provider setup failed: %s", exc)
            self.message_user(
                request,
                _(
                    "Reindexing is unavailable: embedding provider is not "
                    "configured. Please check OPENAI_API_KEY."
                ),
                level="error",
            )
            return

        service = IndexingService(provider)
        success_count = 0
        failure_count = 0

        for document in queryset:
            try:
                service.index_document(document)
                success_count += 1
            except EmbeddingError as exc:
                failure_count += 1
                logger.warning("Admin reindex failed for document %s: %s", document.pk, exc)

        self.message_user(
            request,
            _("Reindexed %(success)d document(s), %(failure)d failed.")
            % {"success": success_count, "failure": failure_count},
        )

    def _create_provider(self) -> OpenAIEmbeddingProvider:
        """Return the production OpenAI embedding provider.

        This factory never falls back to a test provider.
        """
        return OpenAIEmbeddingProvider()


@admin.register(KnowledgeChunk)
class KnowledgeChunkAdmin(admin.ModelAdmin):
    """Diagnostic read-only view of derived chunks."""

    list_display = ("document", "sequence", "created_at")
    list_filter = ("document__language", "document__category")
    search_fields = ("document__title", "content")
    readonly_fields = ("document", "sequence", "content", "embedding", "created_at")
    fields = ("document", "sequence", "content", "created_at")

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
