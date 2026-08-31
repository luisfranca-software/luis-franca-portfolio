"""Purge analytics events that exceeded the configured retention period.

Governing documents: ARCH-001 (15.7), ADR-001 (Release 1.1 analytics).
"""

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.common.models import AnalyticsEvent


class Command(BaseCommand):
    help = "Delete analytics events that exceeded the configured retention period."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--days",
            type=int,
            dest="retention_days",
            help="Retention period in days (overrides ANALYTICS_RETENTION_DAYS).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report how many events would be purged without deleting them.",
        )

    def handle(self, *args, **options) -> None:
        retention_days = options["retention_days"] or settings.ANALYTICS_RETENTION_DAYS
        count = AnalyticsEvent.purge_expired(
            retention_days=retention_days,
            dry_run=options["dry_run"],
        )

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING(f"Would purge {count} analytics event(s)."))
            return

        self.stdout.write(self.style.SUCCESS(f"Purged {count} analytics event(s)."))
