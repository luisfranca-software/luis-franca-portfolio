"""Persistent contact request model for the Contact module.

Governing documents: SPEC-002 (sections 7, 8, 9), ARCH-001 (14.4, 15.7),
ADR-004.
"""

import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CommunicationType(models.TextChoices):
    """Communication type of a contact request (ADR-004)."""

    CONTACT = "contact", _("Contact")
    QUOTATION = "quotation", _("Quotation request")


class RequestStatus(models.TextChoices):
    """Processing status of a contact request (ADR-004)."""

    RECEIVED = "received", _("Received")
    NOTIFIED = "notified", _("Notified")
    NOTIFICATION_FAILED = "notification_failed", _("Notification failed")


class ContactRequest(models.Model):
    """A persisted contact or quotation submission (SPEC-002-REQ-006)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100, verbose_name=_("Full name"))
    email = models.EmailField(max_length=254, verbose_name=_("Email address"))
    subject = models.CharField(max_length=150, verbose_name=_("Subject"))
    message = models.TextField(max_length=4000, verbose_name=_("Message"))
    communication_type = models.CharField(
        max_length=16,
        choices=CommunicationType.choices,
        default=CommunicationType.CONTACT,
        verbose_name=_("Communication type"),
    )
    status = models.CharField(
        max_length=32,
        choices=RequestStatus.choices,
        default=RequestStatus.RECEIVED,
        verbose_name=_("Processing status"),
    )
    submitted_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name=_("Submitted at"),
    )

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = _("contact request")
        verbose_name_plural = _("contact requests")

    def __str__(self) -> str:
        return f"{self.communication_type}:{self.subject} ({self.email})"

    def is_expired(self, retention_days: int | None = None) -> bool:
        """Return whether the request exceeded the approved retention period.

        Retention starts at the submission timestamp (ADR-004).
        """

        days = (
            retention_days
            if retention_days is not None
            else settings.CONTACT_RETENTION_DAYS
        )
        return timezone.now() - self.submitted_at >= timedelta(days=days)
