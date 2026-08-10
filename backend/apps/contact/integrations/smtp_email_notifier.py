"""SMTP transactional email notifier.

Provider-specific behavior is confined to this adapter (Integrations Layer).
The provider is Brevo SMTP relay; configuration is environment-based and
credentials are never hardcoded (ADR-004).

Governing documents: ARCH-001 (12.5, 16.1, 16.2, 20.3), SPEC-002 (section 9),
ADR-004.
"""

import logging

from django.conf import settings
from django.core import mail

from apps.contact.models import CommunicationType, ContactRequest
from apps.contact.services.email_notifier import EmailNotificationError

logger = logging.getLogger(__name__)


class SmtpTransactionalEmailNotifier:
    """Delivers transactional email notifications through Django's SMTP backend."""

    def deliver(self, contact_request: ContactRequest) -> None:
        recipient = settings.CONTACT_NOTIFICATION_EMAIL
        if not recipient:
            logger.warning(
                "Contact request %s has no configured notification recipient",
                contact_request.id,
            )
            raise EmailNotificationError("Notification recipient is not configured")

        try:
            mail.send_mail(
                subject=self._subject_for(contact_request),
                message=self._body_for(contact_request),
                from_email=self._sender(),
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception as exc:
            logger.warning(
                "Email notification delivery failed for contact request %s",
                contact_request.id,
            )
            raise EmailNotificationError("Email notification delivery failed") from exc

    def _sender(self) -> str:
        return (
            settings.DEFAULT_FROM_EMAIL
            or settings.CONTACT_NOTIFICATION_EMAIL
            or "noreply@localhost"
        )

    def _subject_for(self, contact_request: ContactRequest) -> str:
        if contact_request.communication_type == CommunicationType.QUOTATION:
            label = "Quotation request"
        else:
            label = "Contact message"
        return (
            f"[Portfolio] {label} from {contact_request.full_name}: "
            f"{contact_request.subject}"
        )

    def _body_for(self, contact_request: ContactRequest) -> str:
        return (
            f"Request id: {contact_request.id}\n"
            f"Type: {contact_request.get_communication_type_display()}\n"
            f"Name: {contact_request.full_name}\n"
            f"Email: {contact_request.email}\n"
            f"Subject: {contact_request.subject}\n"
            f"Submitted at: {contact_request.submitted_at.isoformat()}\n\n"
            f"Message:\n{contact_request.message}\n"
        )
