"""Shared platform models for the Common module.

Governing documents: ARCH-001 (14.6), ADR-001 (Release 1.1 analytics).
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AnalyticsEvent(models.Model):
    """Privacy-preserving server-side analytics event.

    Release 1.1 requires essential analytics with data minimization. This model
    stores only the event category, public path, active language, and a small
    allowlisted metadata payload. No personally identifiable information is
    collected.
    """

    class EventType(models.TextChoices):
        PAGE_VIEW = "page_view", _("page view")
        PROJECT_INTERACTION = "project_interaction", _("project interaction")
        RESUME_CTA = "resume_cta", _("résumé CTA")
        CONTACT_CTA = "contact_cta", _("Contact CTA")
        CONTACT_SUCCESS = "contact_success", _("successful Contact submission")
        LANGUAGE_CHANGE = "language_change", _("language change")
        PROFESSIONAL_LINK = "professional_link", _("professional link")

    _METADATA_ALLOWLIST: dict[str, dict[str, type]] = {
        EventType.PROJECT_INTERACTION: {"project": str, "action": str},
        EventType.PROFESSIONAL_LINK: {"network": str},
        EventType.LANGUAGE_CHANGE: {"language": str},
        EventType.CONTACT_SUCCESS: {"communication_type": str},
    }
    _MAX_METADATA_KEY_LENGTH = 32
    _MAX_METADATA_VALUE_LENGTH = 128

    event_type = models.CharField(
        max_length=32,
        choices=EventType.choices,
        verbose_name=_("event type"),
    )
    path = models.CharField(
        max_length=255,
        verbose_name=_("path"),
    )
    language = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_("language"),
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("metadata"),
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name=_("created at"),
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("analytics event")
        verbose_name_plural = _("analytics events")
        indexes = [
            models.Index(fields=["event_type", "created_at"]),
            models.Index(fields=["path", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.event_type} @ {self.path} ({self.created_at.isoformat()})"

    @classmethod
    def _validate_path(cls, path: str) -> str:
        """Return a normalized safe path string.

        The path is expected to originate from ``request.path_info`` or another
        server-trusted source. Reject values that are not plausible application
        paths to prevent arbitrary external URLs from being persisted.
        """
        if not isinstance(path, str):
            raise ValueError("path must be a string")

        path = path.strip()
        if not path:
            return "/"

        if len(path) > 255:
            raise ValueError("path exceeds maximum length")

        if not path.startswith("/"):
            raise ValueError("path must be a same-origin absolute path")

        # Reject URLs with authority components, control characters, or
        # directory traversal sequences.
        if "\x00" in path or "//" in path or ".." in path:
            raise ValueError("path contains disallowed sequence")

        return path

    @classmethod
    def _validate_metadata(
        cls,
        event_type: str,
        metadata: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Return a sanitized metadata dict for the given event type.

        Unknown keys are dropped. Known keys must be strings within the defined
        length limits. Invalid structures or oversized values raise
        ``ValueError`` so the caller can reject the event with a 400 response.
        """
        if metadata is None:
            return {}

        if not isinstance(metadata, dict):
            raise ValueError("metadata must be a JSON object")

        allowed = cls._METADATA_ALLOWLIST.get(event_type, {})
        sanitized: dict[str, Any] = {}

        for key, value in metadata.items():
            if not isinstance(key, str):
                raise ValueError("metadata keys must be strings")
            if len(key) > cls._MAX_METADATA_KEY_LENGTH:
                raise ValueError("metadata key exceeds maximum length")
            if key not in allowed:
                # Unsupported keys are dropped rather than persisted.
                continue

            expected_type = allowed[key]
            if not isinstance(value, expected_type):
                raise ValueError(f"metadata value for '{key}' has invalid type")

            if isinstance(value, str) and len(value) > cls._MAX_METADATA_VALUE_LENGTH:
                raise ValueError(f"metadata value for '{key}' exceeds maximum length")

            sanitized[key] = value

        return sanitized

    @classmethod
    def record(
        cls,
        *,
        event_type: str,
        request,
        path: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AnalyticsEvent | None:
        """Persist an analytics event from the current request.

        Returns ``None`` when analytics is disabled in settings.
        """

        from django.conf import settings

        if not getattr(settings, "ANALYTICS_ENABLED", True):
            return None

        safe_path = cls._validate_path(path or request.path_info)
        safe_metadata = cls._validate_metadata(event_type, metadata)

        return cls.objects.create(
            event_type=event_type,
            path=safe_path,
            language=getattr(request, "LANGUAGE_CODE", "") or "",
            metadata=safe_metadata,
        )

    @classmethod
    def purge_expired(
        cls,
        retention_days: int | None = None,
        *,
        dry_run: bool = False,
    ) -> int:
        """Delete analytics events older than the configured retention period.

        Returns the number of events that were (or would be) purged.
        """
        from django.conf import settings

        days = (
            retention_days
            if retention_days is not None
            else getattr(settings, "ANALYTICS_RETENTION_DAYS", 365)
        )
        cutoff = timezone.now() - timedelta(days=days)
        expired = cls.objects.filter(created_at__lt=cutoff)
        count = expired.count()
        if not dry_run:
            expired.delete()
        return count
