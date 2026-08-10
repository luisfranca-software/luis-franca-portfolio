"""Internal transactional email integration contract.

Application workflows depend only on this contract; provider-specific behavior
lives in the Integrations Layer (ARCH-001 12.5, 16.1, 16.2; ADR-004).
"""

from typing import Protocol

from apps.contact.models import ContactRequest


class EmailNotificationError(Exception):
    """Raised when the transactional email notification cannot be delivered."""


class TransactionalEmailNotifier(Protocol):
    """Contract for delivering transactional email notifications."""

    def deliver(self, contact_request: ContactRequest) -> None: ...
