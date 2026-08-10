"""Integration tests for the contact request purge mechanism (ADR-004 6.4)."""

from datetime import timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone

from apps.contact.models import ContactRequest

pytestmark = pytest.mark.django_db


def _create(submitted_at) -> ContactRequest:
    return ContactRequest.objects.create(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Hello",
        message="Message body",
        submitted_at=submitted_at,
    )


def test_purge_deletes_only_expired_requests() -> None:
    expired = _create(timezone.now() - timedelta(days=91))
    recent = _create(timezone.now() - timedelta(days=1))

    call_command("purge_contact_requests")

    assert ContactRequest.objects.filter(pk=expired.pk).exists() is False
    assert ContactRequest.objects.filter(pk=recent.pk).exists() is True


def test_purge_dry_run_does_not_delete() -> None:
    expired = _create(timezone.now() - timedelta(days=91))

    call_command("purge_contact_requests", "--dry-run")

    assert ContactRequest.objects.filter(pk=expired.pk).exists() is True


def test_purge_respects_days_override() -> None:
    old = _create(timezone.now() - timedelta(days=100))

    call_command("purge_contact_requests", "--days", "365")
    assert ContactRequest.objects.filter(pk=old.pk).exists() is True

    call_command("purge_contact_requests", "--days", "90")
    assert ContactRequest.objects.filter(pk=old.pk).exists() is False


def test_purge_is_idempotent() -> None:
    _create(timezone.now() - timedelta(days=95))

    call_command("purge_contact_requests")
    call_command("purge_contact_requests")

    assert ContactRequest.objects.count() == 0
