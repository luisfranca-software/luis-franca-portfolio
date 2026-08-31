"""Purge analytics events that exceeded the configured retention period.

Governing documents: ARCH-001 (15.7), ADR-001 (Release 1.1 analytics).
"""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

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
        retention_days = options["retention_days"]
        if retention_days is None:
            retention_days = settings.ANALYTICS_RETENTION_DAYS

        if not isinstance(retention_days, int) or retention_days < 1:
            raise CommandError("retention_days must be a positive integer")

        try:
            count = AnalyticsEvent.purge_expired(
                retention_days=retention_days,
                dry_run=options["dry_run"],
            )
        except ValueError as exc:
            raise CommandError(str(exc)) from exc

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING(f"Would purge {count} analytics event(s)."))
            return

        self.stdout.write(self.style.SUCCESS(f"Purged {count} analytics event(s)."))
