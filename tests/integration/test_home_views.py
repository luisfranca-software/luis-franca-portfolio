"""Integration tests for the Home page (SPEC-001-REQ-003)."""

from django.test import Client


def test_home_page_renders() -> None:
    response = Client().get("/")

    assert response.status_code == 200


def test_home_page_presents_approved_identity() -> None:
    content = Client().get("/").content.decode()

    assert "Luís França" in content
    assert "Luís Eduardo Carvalho França" in content


def test_home_page_presents_all_approved_titles() -> None:
    content = Client().get("/").content.decode()

    assert "Software Engineer" in content
    assert "Python Backend Engineer" in content
    assert "AI/LLM Engineer" in content


def test_home_page_presents_primary_cta() -> None:
    content = Client().get("/").content.decode()

    assert "Let's Talk" in content
    assert 'href="/contact/"' in content


def test_home_page_includes_profile_photo() -> None:
    content = Client().get("/").content.decode()

    assert "images/profile/luis-franca" in content
    assert "Professional photograph of Luís Eduardo Carvalho França" in content
