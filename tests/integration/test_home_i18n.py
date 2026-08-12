"""Integration tests for Home page bilingual behavior (SPEC-001 section 8)."""

from django.test import Client


def test_home_page_renders_in_english_by_default() -> None:
    content = Client().get("/").content.decode()

    assert "Hello, I'm" in content
    assert "Let's Talk" in content
    assert "Vamos conversar" not in content


def test_home_page_renders_in_portuguese() -> None:
    client = Client(HTTP_ACCEPT_LANGUAGE="pt-br")
    response = client.get("/")
    content = response.content.decode()

    assert "Olá, eu sou" in content
    assert "Vamos conversar" in content
    assert "Engenheiro de Software" in content
