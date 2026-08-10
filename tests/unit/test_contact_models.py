"""Unit tests for the ContactRequest model (SPEC-002-REQ-006, ADR-004)."""

from datetime import timedelta

import pytest
from django.utils import timezone

from apps.contact.models import (
    CommunicationType,
    ContactRequest,
    RequestStatus,
)

pytestmark = pytest.mark.django_db


def test_communication_type_choices_cover_contact_and_quotation() -> None:
    assert CommunicationType.values == ["contact", "quotation"]


def test_request_status_choices_cover_approved_states() -> None:
    assert RequestStatus.values == [
        "received",
        "notified",
        "notification_failed",
    ]


def test_contact_request_defaults() -> None:
    contact_request = ContactRequest.objects.create(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Hello",
        message="Message body",
    )
    assert contact_request.communication_type == CommunicationType.CONTACT
    assert contact_request.status == RequestStatus.RECEIVED
    assert contact_request.submitted_at is not None
    assert contact_request.id is not None


def test_contact_request_persists_quotation_type() -> None:
    contact_request = ContactRequest.objects.create(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Budget",
        message="Quotation message",
        communication_type=CommunicationType.QUOTATION,
    )
    assert contact_request.communication_type == CommunicationType.QUOTATION


def test_is_expired_false_within_retention() -> None:
    contact_request = ContactRequest.objects.create(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Hello",
        message="Message body",
        submitted_at=timezone.now() - timedelta(days=30),
    )
    assert contact_request.is_expired() is False


def test_is_expired_true_beyond_retention() -> None:
    contact_request = ContactRequest.objects.create(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Hello",
        message="Message body",
        submitted_at=timezone.now() - timedelta(days=91),
    )
    assert contact_request.is_expired() is True


def test_is_expired_respects_explicit_retention_days() -> None:
    contact_request = ContactRequest.objects.create(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Hello",
        message="Message body",
        submitted_at=timezone.now() - timedelta(days=100),
    )
    assert contact_request.is_expired(retention_days=90) is True
    assert contact_request.is_expired(retention_days=365) is False
