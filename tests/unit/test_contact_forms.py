"""Unit tests for the ContactForm (SPEC-002-REQ-002, REQ-003, REQ-004)."""

from apps.contact.forms import ContactForm
from apps.contact.models import CommunicationType

VALID_PAYLOAD = {
    "full_name": "Ana Souza",
    "email": "ana@example.test",
    "subject": "Project inquiry",
    "message": "I would like to discuss a project.",
}


def test_form_accepts_valid_contact_submission() -> None:
    form = ContactForm(data=VALID_PAYLOAD)
    assert form.is_valid()
    assert form.cleaned_data["communication_type"] == CommunicationType.CONTACT


def test_form_accepts_valid_quotation_submission() -> None:
    payload = {**VALID_PAYLOAD, "communication_type": CommunicationType.QUOTATION}
    form = ContactForm(data=payload)
    assert form.is_valid()
    assert form.cleaned_data["communication_type"] == CommunicationType.QUOTATION


def test_form_requires_mandatory_fields() -> None:
    for field in ("full_name", "email", "subject", "message"):
        payload = dict(VALID_PAYLOAD)
        payload[field] = ""
        form = ContactForm(data=payload)
        assert form.is_valid() is False
        assert field in form.errors


def test_form_rejects_invalid_email_format() -> None:
    payload = {**VALID_PAYLOAD, "email": "not-an-email"}
    form = ContactForm(data=payload)
    assert form.is_valid() is False
    assert "email" in form.errors


def test_form_enforces_maximum_field_lengths() -> None:
    payload = {**VALID_PAYLOAD, "subject": "x" * 151}
    form = ContactForm(data=payload)
    assert form.is_valid() is False
    assert "subject" in form.errors

    payload = {**VALID_PAYLOAD, "message": "x" * 4001}
    form = ContactForm(data=payload)
    assert form.is_valid() is False
    assert "message" in form.errors


def test_form_strips_surrounding_whitespace() -> None:
    payload = {
        **VALID_PAYLOAD,
        "full_name": "  Ana Souza  ",
        "subject": "  Project inquiry  ",
    }
    form = ContactForm(data=payload)
    assert form.is_valid()
    assert form.cleaned_data["full_name"] == "Ana Souza"
    assert form.cleaned_data["subject"] == "Project inquiry"


def test_form_rejects_blank_after_strip() -> None:
    payload = {**VALID_PAYLOAD, "full_name": "   "}
    form = ContactForm(data=payload)
    assert form.is_valid() is False
    assert "full_name" in form.errors


def test_form_removes_control_characters() -> None:
    payload = {
        **VALID_PAYLOAD,
        "subject": "Project\x01inquiry",
        "message": "Body\x1bwith\x07control characters",
    }
    form = ContactForm(data=payload)
    assert form.is_valid()
    assert form.cleaned_data["subject"] == "Projectinquiry"
    assert form.cleaned_data["message"] == "Bodywithcontrol characters"


def test_form_preserves_newlines_in_message() -> None:
    payload = {**VALID_PAYLOAD, "message": "Line one\nLine two"}
    form = ContactForm(data=payload)
    assert form.is_valid()
    assert form.cleaned_data["message"] == "Line one\nLine two"


def test_form_rejects_unknown_communication_type() -> None:
    payload = {**VALID_PAYLOAD, "communication_type": "unknown"}
    form = ContactForm(data=payload)
    assert form.is_valid() is False
    assert "communication_type" in form.errors
