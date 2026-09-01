"""Purge IA Jujuju conversations older than the configured retention period.

Governing documents: SPEC-005 §42–43.
"""

from __future__ import annotations

import logging
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.assistant.models import Conversation

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Remove expired IA Jujuju conversations and dependent data."""

    help = "Purge IA Jujuju conversations older than ASSISTANT_RETENTION_DAYS"

    def handle(self, *args, **options):
        retention_days = int(getattr(settings, "ASSISTANT_RETENTION_DAYS", 90))
        cutoff = timezone.now() - timedelta(days=retention_days)
        queryset = Conversation.objects.filter(created_at__lt=cutoff)
        count, _ = queryset.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Purged {count} expired conversation(s) older than {retention_days} days."
            )
        )
        logger.info(
            "Purged %d expired IA Jujuju conversation(s) older than %d days.",
            count,
            retention_days,
        )
