"""Shared pytest fixtures for the SPEC-002 Contact & Communication tests.

The transactional email provider decision (ADR-004) is exercised through test
substitution: the locmem email backend captures notifications without a live
provider connection (ARCH-001 16.2).
"""

import pytest
from django.conf import settings as django_settings
from django.core import mail
from django.test import override_settings


@pytest.fixture(autouse=True)
def _disable_analytics():
    """Disable analytics by default to avoid DB writes in non-DB tests."""
    original = getattr(django_settings, "ANALYTICS_ENABLED", True)
    django_settings.ANALYTICS_ENABLED = False
    yield
    django_settings.ANALYTICS_ENABLED = original


@pytest.fixture
def email_backend():
    """Substitute the email backend with the in-memory locmem backend."""

    with override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="portfolio@example.test",
        CONTACT_NOTIFICATION_EMAIL="owner@example.test",
    ):
        yield


@pytest.fixture(scope="session")
def django_db_modify_db_settings():
    """Use a prepared template database that already has the pgvector extension.

    The application database user is not a PostgreSQL superuser and therefore
    cannot execute ``CREATE EXTENSION vector`` inside the test database created
    by pytest-django. The template ``test_template_luis_franca_portfolio`` is
    provisioned separately with the extension and a clean schema.
    """
    from django.conf import settings

    settings.DATABASES["default"].setdefault("TEST", {})
    settings.DATABASES["default"]["TEST"]["TEMPLATE"] = "test_template_luis_franca_portfolio"


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
        "whatsapp": "https://wa.me/5531993423501",
        "linkedin": "https://www.linkedin.com/in/luisfranca-software/",
        "github": "https://github.com/luisfranca-software",
        "resume": "https://drive.google.com/file/d/1ZbhGxvtm_J7OWF2uXthPN01TSx-Xquav/view?usp=sharing",
    }
    return settings.CONTACT_LINKS
