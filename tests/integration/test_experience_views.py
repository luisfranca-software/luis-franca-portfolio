"""Integration tests for the Experience section (SPEC-001-REQ-006)."""

from django.test import Client


def test_experience_page_renders() -> None:
    response = Client().get("/experience/")

    assert response.status_code == 200


def test_experience_page_presents_career_summary() -> None:
    content = Client().get("/experience/").content.decode()

    assert "more than 20 years of experience" in content
    assert "DC Arquitetura" in content
    assert "LF Information System" in content
    assert "AutoLISP" in content


def test_experience_page_includes_linkedin_entry_point(contact_links) -> None:
    content = Client().get("/experience/").content.decode()

    assert contact_links["linkedin"] in content
    assert "View full profile on LinkedIn" in content
