"""Acceptance tests for SPEC-002 — Contact & Communication (section 11).

Acceptance is based on objective evidence produced through the automated test
suite, aligned with TST-001 and SPEC-002 acceptance criteria.
"""

import pytest
from django.core import mail
from django.test import Client

from apps.contact.models import CommunicationType, ContactRequest, RequestStatus

pytestmark = pytest.mark.django_db


def test_contact_form_operates_correctly_end_to_end(email_backend) -> None:
    client = Client()

    page = client.get("/contact/")
    assert page.status_code == 200

    response = client.post(
        "/contact/",
        {
            "full_name": "Recruiter Name",
            "email": "recruiter@example.test",
            "subject": "Opportunity",
            "message": "We have an interesting position.",
        },
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "/contact/success/"

    contact_request = ContactRequest.objects.get()
    assert contact_request.full_name == "Recruiter Name"
    assert contact_request.email == "recruiter@example.test"
    assert contact_request.status == RequestStatus.NOTIFIED
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["owner@example.test"]

    confirmation = client.get(response.headers["Location"])
    assert confirmation.status_code == 200
    assert "Message sent" in confirmation.content.decode()


def test_quotation_request_workflow(email_backend) -> None:
    response = Client().post(
        "/contact/",
        {
            "full_name": "Client Name",
            "email": "client@example.test",
            "subject": "Quotation",
            "message": "I would like a quotation.",
            "communication_type": CommunicationType.QUOTATION,
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/contact/success/"
    contact_request = ContactRequest.objects.get()
    assert contact_request.communication_type == CommunicationType.QUOTATION
    assert contact_request.status == RequestStatus.NOTIFIED
    assert "Quotation request" in mail.outbox[0].subject


def test_submissions_are_persisted() -> None:
    Client().post(
        "/contact/",
        {
            "full_name": "Persisted Name",
            "email": "persisted@example.test",
            "subject": "Persistence",
            "message": "This request must be persisted.",
        },
    )

    contact_request = ContactRequest.objects.get()
    assert contact_request.full_name == "Persisted Name"
    assert contact_request.subject == "Persistence"
    assert contact_request.submitted_at is not None


def test_whatsapp_and_professional_links_are_present(contact_links) -> None:
    content = Client().get("/contact/").content.decode()

    assert "whatsapp-button" in content
    assert "https://wa.me/5511999999999" in content
    assert "https://www.linkedin.com/in/luis-franca-example" in content
    assert "https://github.com/luis-franca-example" in content


def test_resume_download_references_external_storage(contact_links) -> None:
    content = Client().get("/contact/").content.decode()

    assert "https://drive.google.com/file/d/example/view" in content
