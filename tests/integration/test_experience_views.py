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


def test_experience_page_includes_education_summary() -> None:
    content = Client().get("/experience/").content.decode()

    assert "Software Engineering — In progress" in content
    assert "Building Construction Technician" in content


def test_experience_page_renders_education_in_portuguese() -> None:
    client = Client(HTTP_ACCEPT_LANGUAGE="pt-br")
    content = client.get("/experience/").content.decode()

    assert "Engenharia de Software — Em andamento" in content
    assert "Técnico em Edificações" in content
    # English versions must not remain when Portuguese is active.
    assert "Software Engineering — In progress" not in content
    assert "Building Construction Technician" not in content


def test_experience_page_does_not_show_training_section() -> None:
    content = Client().get("/experience/").content.decode()

    assert "Python Impressionador" not in content
    assert "Python Master" not in content
    assert "IA Master" not in content
    assert "API Master" not in content


def test_experience_page_does_not_show_milestones_section() -> None:
    content = Client().get("/experience/").content.decode()

    # DC Arquitetura and LF Information System remain in the career narrative,
    # but must not appear as a separate milestone list.
    assert content.count("Milestones") == 0


def test_experience_page_includes_linkedin_entry_point(contact_links) -> None:
    content = Client().get("/experience/").content.decode()

    assert contact_links["linkedin"] in content
    assert "View full profile on LinkedIn" in content
