"""Integration tests for the Contact views and URLs (SPEC-002).

Verifies the full submission workflow: GET form, POST validation, persistence,
transactional email generation and the controlled success/failure confirmation
views (SPEC-002 section 7, ARCH-001 22.3).
"""

import pytest
from django.core import mail
from django.test import Client, override_settings

from apps.contact.models import CommunicationType, ContactRequest, RequestStatus

pytestmark = pytest.mark.django_db

VALID_PAYLOAD = {
    "full_name": "Ana Souza",
    "email": "ana@example.test",
    "subject": "Project inquiry",
    "message": "I would like to discuss a project.",
}


class FailingEmailBackend:
    """Simulates a provider outage during delivery (ARCH-001 16.4)."""

    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        self.fail_silently = fail_silently

    def send_messages(self, email_messages) -> None:
        raise OSError("simulated provider outage")


def test_contact_page_renders_the_form() -> None:
    response = Client().get("/contact/")

    assert response.status_code == 200
    content = response.content.decode()
    assert 'name="full_name"' in content
    assert 'name="email"' in content
    assert 'name="subject"' in content
    assert 'name="communication_type"' in content
    assert 'name="message"' in content
    assert "csrfmiddlewaretoken" in content


def test_valid_submission_redirects_to_success_and_emails(email_backend) -> None:
    response = Client().post("/contact/", VALID_PAYLOAD)

    assert response.status_code == 302
    assert response.headers["Location"] == "/contact/success/"
    contact_request = ContactRequest.objects.get()
    assert contact_request.status == RequestStatus.NOTIFIED
    assert contact_request.communication_type == CommunicationType.CONTACT
    assert contact_request.full_name == "Ana Souza"
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["owner@example.test"]


def test_valid_quotation_submission(email_backend) -> None:
    payload = {
        **VALID_PAYLOAD,
        "communication_type": CommunicationType.QUOTATION,
        "subject": "Budget for a website",
    }
    response = Client().post("/contact/", payload)

    assert response.status_code == 302
    assert response.headers["Location"] == "/contact/success/"
    contact_request = ContactRequest.objects.get()
    assert contact_request.communication_type == CommunicationType.QUOTATION
    assert "Quotation request" in mail.outbox[0].subject


def test_invalid_submission_rerenders_form_with_errors() -> None:
    payload = {**VALID_PAYLOAD, "email": "not-an-email"}
    response = Client().post("/contact/", payload)

    assert response.status_code == 200
    content = response.content.decode()
    assert "email" in content
    assert ContactRequest.objects.count() == 0
    assert mail.outbox == []


def test_notification_failure_redirects_to_failure_page(email_backend) -> None:
    with override_settings(
        EMAIL_BACKEND="tests.integration.test_contact_views.FailingEmailBackend"
    ):
        response = Client().post("/contact/", VALID_PAYLOAD)

    assert response.status_code == 302
    assert response.headers["Location"] == "/contact/failure/"
    contact_request = ContactRequest.objects.get()
    assert contact_request.status == RequestStatus.NOTIFICATION_FAILED


def test_success_page_renders_confirmation() -> None:
    response = Client().get("/contact/success/")

    assert response.status_code == 200
    assert "Message sent" in response.content.decode()


def test_failure_page_renders_controlled_message() -> None:
    response = Client().get("/contact/failure/")

    assert response.status_code == 200
    content = response.content.decode()
    assert "Message received" in content
    assert "stack" not in content.lower()


def test_contact_page_includes_professional_links(contact_links) -> None:
    response = Client().get("/contact/")
    content = response.content.decode()

    assert "https://www.linkedin.com/in/luisfranca-software/" in content
    assert "https://github.com/luisfranca-software" in content
    assert "https://wa.me/5531993423501" in content
    resume_url = (
        "https://drive.google.com/file/d/"
        "1ZbhGxvtm_J7OWF2uXthPN01TSx-Xquav/view?usp=sharing"
    )
    assert resume_url in content


def test_floating_whatsapp_button_rendered(contact_links) -> None:
    response = Client().get("/contact/")
    content = response.content.decode()

    assert "whatsapp-button" in content
    assert "https://wa.me/5531993423501" in content


def test_floating_whatsapp_button_hidden_when_not_configured() -> None:
    response = Client().get("/contact/")
    assert "whatsapp-button" not in response.content.decode()


def test_post_without_csrf_token_is_rejected() -> None:
    client = Client(enforce_csrf_checks=True)
    response = client.post("/contact/", VALID_PAYLOAD)

    assert response.status_code == 403
    assert ContactRequest.objects.count() == 0
