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
