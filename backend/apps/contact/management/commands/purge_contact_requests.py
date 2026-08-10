"""Purge contact requests that exceeded the approved retention period.

Governing documents: ARCH-001 (15.7), SPEC-002 (section 8), ADR-004 (6.4).
"""

from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.contact.models import ContactRequest


class Command(BaseCommand):
    help = "Delete contact requests that exceeded the approved retention period."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--days",
            type=int,
            dest="retention_days",
            help="Retention period in days (overrides CONTACT_RETENTION_DAYS).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report how many requests would be purged without deleting them.",
        )

    def handle(self, *args, **options) -> None:
        retention_days = options["retention_days"] or settings.CONTACT_RETENTION_DAYS
        cutoff = timezone.now() - timedelta(days=retention_days)
        expired = ContactRequest.objects.filter(submitted_at__lt=cutoff)
        count = expired.count()

        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING(f"Would purge {count} contact request(s).")
            )
            return

        expired.delete()
        self.stdout.write(self.style.SUCCESS(f"Purged {count} contact request(s)."))
