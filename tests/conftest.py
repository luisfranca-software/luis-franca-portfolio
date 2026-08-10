"""Shared pytest fixtures for the SPEC-002 Contact & Communication tests.

The transactional email provider decision (ADR-004) is exercised through test
substitution: the locmem email backend captures notifications without a live
provider connection (ARCH-001 16.2).
"""

import pytest
from django.core import mail
from django.test import override_settings


@pytest.fixture
def email_backend():
    """Substitute the email backend with the in-memory locmem backend."""

    with override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="portfolio@example.test",
        CONTACT_NOTIFICATION_EMAIL="owner@example.test",
    ):
        yield


@pytest.fixture(autouse=True)
def _reset_mail_outbox():
    outbox = getattr(mail, "outbox", None)
    if outbox is not None:
        outbox.clear()
    yield
    outbox = getattr(mail, "outbox", None)
    if outbox is not None:
        outbox.clear()


@pytest.fixture
def contact_links(settings):
    """Configure externalized public professional links (ARCH-001 16.3)."""

    settings.CONTACT_LINKS = {
        "whatsapp": "https://wa.me/5511999999999",
        "linkedin": "https://www.linkedin.com/in/luis-franca-example",
        "github": "https://github.com/luis-franca-example",
        "resume": "https://drive.google.com/file/d/example/view",
    }
