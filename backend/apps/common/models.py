"""Shared platform models for the Common module.

Governing documents: ARCH-001 (14.6), ADR-001 (Release 1.1 analytics).
"""

from __future__ import annotations

import hashlib
from typing import Any

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AnalyticsEvent(models.Model):
    """Privacy-preserving server-side analytics event.

    Release 1.1 requires essential analytics with data minimization. This model
    stores only the event category, public path, active language, and an
    anonymized session fingerprint. No personally identifiable information is
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
    session_fingerprint = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_("session fingerprint"),
        help_text=_("SHA-256 hash of the Django session key; no PII is stored."),
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

        session_key = getattr(request.session, "session_key", None) or ""
        fingerprint = (
            hashlib.sha256(session_key.encode()).hexdigest() if session_key else ""
        )
        return cls.objects.create(
            event_type=event_type,
            path=path or request.path_info,
            language=getattr(request, "LANGUAGE_CODE", "") or "",
            session_fingerprint=fingerprint,
            metadata=metadata or {},
        )
