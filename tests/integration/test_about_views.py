"""Integration tests for the About section (SPEC-001-REQ-004)."""

from django.test import Client


def test_about_page_renders() -> None:
    response = Client().get("/about/")

    assert response.status_code == 200


def test_about_page_presents_approved_summary() -> None:
    content = Client().get("/about/").content.decode()

    assert "I am a Software Engineer specializing in Python backend development" in content
    assert "specification, architecture, implementation, automated testing" in content
    assert "engineering decision rather than an end in itself" in content
