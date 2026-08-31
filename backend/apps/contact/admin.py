"""Django Admin registration for the Contact module.

Governing documents: SPEC-002 (sections 7, 8, 9), ARCH-001 (17.9),
ADR-001 (Release 2 — Platform Evolution).

ContactRequest is exposed as a read-oriented administrative view. The Django
Admin surface is intentionally not a CRM: submissions are visible for
operational awareness, but creation, editing, and deletion are disabled to
preserve the approved Contact lifecycle and retention behavior.
"""

from __future__ import annotations

from django.contrib import admin

from apps.contact.models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    """Read-oriented admin visibility for contact/quotation submissions."""

    list_display = (
        "full_name",
        "email",
        "subject",
        "communication_type",
        "status",
        "submitted_at",
    )
    list_filter = ("communication_type", "status", "submitted_at")
    search_fields = ("full_name", "email", "subject")
    readonly_fields = (
        "id",
        "full_name",
        "email",
        "subject",
        "message",
        "communication_type",
        "status",
        "submitted_at",
    )
    ordering = ("-submitted_at",)

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
