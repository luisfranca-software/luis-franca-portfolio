"""Django Admin registration for IA Jujuju conversation data.

Governing documents: ADR-007 §21; SPEC-005 §40–41.
"""

from __future__ import annotations

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.assistant.models import Conversation, ConversationMessage, SourceEvidence


class ConversationMessageInline(admin.TabularInline):
    """Read-only diagnostic view of conversation messages."""

    model = ConversationMessage
    extra = 0
    fields = ("sequence", "role", "content", "created_at")
    readonly_fields = ("sequence", "role", "content", "created_at")
    can_delete = False
    show_change_link = False

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


class SourceEvidenceInline(admin.TabularInline):
    """Read-only diagnostic view of retrieval/source evidence."""

    model = SourceEvidence
    extra = 0
    fields = (
        "rank",
        "distance",
        "document_title",
        "document_slug",
        "document_language",
        "document_category",
        "chunk_content",
        "retrieved_at",
    )
    readonly_fields = fields
    can_delete = False
    show_change_link = False

    def has_add_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Diagnostic read-oriented inspection of conversations."""

    list_display = (
        "pk",
        "language",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "language",
        "status",
        "created_at",
    )
    search_fields = ("pk", "session_key")
    readonly_fields = (
        "session_key",
        "language",
        "status",
        "created_at",
        "updated_at",
    )
    inlines = [ConversationMessageInline]
    fieldsets = (
        (
            None,
            {
                "fields": ("language", "status"),
            },
        ),
        (
            _("Operational metadata"),
            {
                "fields": ("session_key",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    """Diagnostic read-oriented inspection of messages."""

    list_display = (
        "pk",
        "conversation",
        "sequence",
        "role",
        "created_at",
    )
    list_filter = (
        "role",
        "created_at",
        "conversation__language",
        "conversation__status",
    )
    search_fields = ("content", "conversation__session_key")
    readonly_fields = (
        "conversation",
        "sequence",
        "role",
        "content",
        "created_at",
    )
    inlines = [SourceEvidenceInline]
    fields = readonly_fields

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser


@admin.register(SourceEvidence)
class SourceEvidenceAdmin(admin.ModelAdmin):
    """Diagnostic read-oriented inspection of source evidence."""

    list_display = (
        "pk",
        "message",
        "rank",
        "distance",
        "document_title",
        "document_language",
        "document_category",
        "retrieved_at",
    )
    list_filter = (
        "document_language",
        "document_category",
        "retrieved_at",
    )
    search_fields = (
        "document_title",
        "document_slug",
        "chunk_content",
    )
    readonly_fields = (
        "message",
        "document",
        "chunk",
        "rank",
        "distance",
        "document_title",
        "document_slug",
        "document_language",
        "document_category",
        "chunk_content",
        "retrieved_at",
    )
    fields = readonly_fields

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return request.user.is_superuser
