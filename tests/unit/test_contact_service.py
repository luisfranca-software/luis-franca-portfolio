"""Unit tests for the ContactService (SPEC-002 section 7 workflow, ADR-004)."""

from dataclasses import dataclass

import pytest

from apps.contact.models import CommunicationType, ContactRequest, RequestStatus
from apps.contact.services.contact_service import ContactService
from apps.contact.services.email_notifier import EmailNotificationError

pytestmark = pytest.mark.django_db


@dataclass
class RecordingNotifier:
    """Test double implementing the internal integration contract."""

    deliveries: list[ContactRequest]
    fail: bool = False

    def deliver(self, contact_request: ContactRequest) -> None:
        if self.fail:
            raise EmailNotificationError("simulated provider failure")
        self.deliveries.append(contact_request)


def test_submit_persists_received_then_notifies() -> None:
    deliveries: list[ContactRequest] = []
    service = ContactService(email_notifier=RecordingNotifier(deliveries=deliveries))

    result = service.submit(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Hello",
        message="Message body",
    )

    assert result.status == RequestStatus.NOTIFIED
    assert deliveries == [result]
    persisted = ContactRequest.objects.get(pk=result.pk)
    assert persisted.status == RequestStatus.NOTIFIED


def test_submit_persists_quotation_and_notifies() -> None:
    deliveries: list[ContactRequest] = []
    service = ContactService(email_notifier=RecordingNotifier(deliveries=deliveries))

    result = service.submit(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Budget",
        message="Quotation message",
        communication_type=CommunicationType.QUOTATION,
    )

    assert result.status == RequestStatus.NOTIFIED
    persisted = ContactRequest.objects.get(pk=result.pk)
    assert persisted.communication_type == CommunicationType.QUOTATION


def test_submit_keeps_request_when_notification_fails() -> None:
    service = ContactService(
        email_notifier=RecordingNotifier(deliveries=[], fail=True)
    )

    result = service.submit(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Hello",
        message="Message body",
    )

    assert result.status == RequestStatus.NOTIFICATION_FAILED
    persisted = ContactRequest.objects.get(pk=result.pk)
    assert persisted.status == RequestStatus.NOTIFICATION_FAILED
    assert ContactRequest.objects.filter(pk=result.pk).exists()
