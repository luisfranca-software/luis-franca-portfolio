"""Integration tests for the Skills section (SPEC-001-REQ-005)."""

import html

from django.test import Client

from apps.skills.skills import SKILL_GROUPS


def test_skills_page_renders() -> None:
    response = Client().get("/skills/")

    assert response.status_code == 200


def test_skills_page_presents_all_approved_groups() -> None:
    content = html.unescape(Client().get("/skills/").content.decode())

    for group in SKILL_GROUPS:
        assert group.name in content
        for skill in group.skills:
            assert skill in content


def test_skills_page_uses_semantic_cards() -> None:
    content = Client().get("/skills/").content.decode()

    assert content.count("<article") == len(SKILL_GROUPS)


def test_skills_page_renders_group_names_in_portuguese() -> None:
    client = Client(HTTP_ACCEPT_LANGUAGE="pt-br")
    content = html.unescape(client.get("/skills/").content.decode())

    assert "Engenharia de Software" in content
    assert "Backend e Python" in content
    assert "Desenvolvimento Desktop" in content
    # English labels must not remain where Portuguese translations exist.
    assert "Software Engineering" not in content
    assert "Backend & Python" not in content
    assert "Desktop Development" not in content


def test_skills_page_renders_skills_in_portuguese() -> None:
    client = Client(HTTP_ACCEPT_LANGUAGE="pt-br")
    content = html.unescape(client.get("/skills/").content.decode())

    assert "Arquitetura de Software" in content
    assert "Programação Orientada a Objetos" in content
    assert "Testes Automatizados" in content
    assert "Integração com LLMs" in content
    # English labels must not remain where Portuguese translations exist.
    assert "Software Architecture" not in content
    assert "Object-Oriented Programming" not in content
    assert "Automated Testing" not in content
    assert "LLM Integration" not in content
