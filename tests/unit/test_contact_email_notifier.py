"""Unit tests for the SMTP transactional email notifier (ADR-004, ARCH-001 16.1).

Provider behavior is exercised through test substitution (locmem backend).
"""

import pytest
from django.core import mail
from django.test import override_settings

from apps.contact.integrations.smtp_email_notifier import (
    SmtpTransactionalEmailNotifier,
)
from apps.contact.models import CommunicationType, ContactRequest
from apps.contact.services.email_notifier import EmailNotificationError


class FailingEmailBackend:
    """Simulates a provider outage during delivery (ARCH-001 16.4)."""

    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        self.fail_silently = fail_silently

    def send_messages(self, email_messages) -> None:
        raise OSError("simulated provider outage")


@pytest.fixture
def contact_request(email_backend) -> ContactRequest:
    return ContactRequest(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Project inquiry",
        message="Message body",
    )


def test_deliver_sends_notification(contact_request: ContactRequest) -> None:
    SmtpTransactionalEmailNotifier().deliver(contact_request)

    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    assert message.to == ["owner@example.test"]
    assert message.from_email == "portfolio@example.test"
    assert "Project inquiry" in message.subject
    assert "Message body" in message.body
    assert "ana@example.test" in message.body


def test_deliver_uses_quotation_subject(email_backend) -> None:
    quotation = ContactRequest(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Budget",
        message="Quotation message",
        communication_type=CommunicationType.QUOTATION,
    )

    SmtpTransactionalEmailNotifier().deliver(quotation)

    assert len(mail.outbox) == 1
    assert "Quotation request" in mail.outbox[0].subject


def test_deliver_raises_when_recipient_not_configured(
    contact_request: ContactRequest,
) -> None:
    with override_settings(CONTACT_NOTIFICATION_EMAIL=""):
        with pytest.raises(EmailNotificationError):
            SmtpTransactionalEmailNotifier().deliver(contact_request)
    assert mail.outbox == []


def test_deliver_raises_controlled_error_on_provider_failure(
    email_backend,
) -> None:
    with override_settings(
        EMAIL_BACKEND="tests.unit.test_contact_email_notifier.FailingEmailBackend"
    ):
        with pytest.raises(EmailNotificationError):
            SmtpTransactionalEmailNotifier().deliver(
                ContactRequest(
                    id="3f2d0f6c-2b4a-4e6c-9c1a-000000000001",
                    full_name="Ana Souza",
                    email="ana@example.test",
                    subject="Hello",
                    message="Message body",
                )
            )
    assert mail.outbox == []
