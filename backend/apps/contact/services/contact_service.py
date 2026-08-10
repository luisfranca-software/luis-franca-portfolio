"""Contact application service.

Governing documents: SPEC-002 (section 7 workflow), ARCH-001 (14.4, 22.3),
ADR-004 (6.5 communication model).
"""

import logging

from apps.contact.models import CommunicationType, ContactRequest, RequestStatus
from apps.contact.services.email_notifier import EmailNotificationError, TransactionalEmailNotifier

logger = logging.getLogger(__name__)


class ContactService:
    """Coordinates persistence and notification for contact requests.

    The service persists the request first (RECEIVED), then delivers the
    transactional email notification through the internal integration contract.
    Delivery outcome is recorded in the processing status (ADR-004 6.5).
    """

    def __init__(self, email_notifier: TransactionalEmailNotifier) -> None:
        self.email_notifier = email_notifier

    def submit(
        self,
        *,
        full_name: str,
        email: str,
        subject: str,
        message: str,
        communication_type: str = CommunicationType.CONTACT,
    ) -> ContactRequest:
        """Persist a contact request and attempt its notification."""

        contact_request = ContactRequest.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message,
            communication_type=communication_type,
            status=RequestStatus.RECEIVED,
        )
        self._notify(contact_request)
        return contact_request

    def _notify(self, contact_request: ContactRequest) -> None:
        try:
            self.email_notifier.deliver(contact_request)
        except EmailNotificationError:
            contact_request.status = RequestStatus.NOTIFICATION_FAILED
            contact_request.save(update_fields=["status"])
            logger.warning("Contact request %s persisted without notification", contact_request.id)
        else:
            contact_request.status = RequestStatus.NOTIFIED
            contact_request.save(update_fields=["status"])
