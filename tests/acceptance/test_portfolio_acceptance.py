"""Acceptance tests for SPEC-003 — Portfolio & Projects (section 12).

Acceptance is based on objective evidence produced through the automated test
suite, aligned with TST-001 and the SPEC-003 acceptance criteria.
"""

from pathlib import Path

from django.test import Client

from apps.portfolio.projects import FEATURED_PROJECTS

REPO_ROOT = Path(__file__).resolve().parents[2]
PORTFOLIO_CSS = REPO_ROOT / "frontend" / "static" / "css" / "portfolio.css"


def test_portfolio_section_is_available() -> None:
    response = Client().get("/portfolio/")

    assert response.status_code == 200


def test_three_featured_projects_are_displayed() -> None:
    content = Client().get("/portfolio/").content.decode()

    assert len(FEATURED_PROJECTS) == 3
    assert content.count("<article") == 3


def test_project_cards_are_reusable() -> None:
    content = Client().get("/portfolio/").content.decode()

    assert content.count("class=\"project-card\"") == len(FEATURED_PROJECTS)


def test_hover_elevation_effects_function() -> None:
    css = PORTFOLIO_CSS.read_text(encoding="utf-8")

    assert ".project-card:hover" in css
    assert "transition:" in css
    assert "box-shadow" in css


def test_screenshot_scrolling_operates() -> None:
    css = PORTFOLIO_CSS.read_text(encoding="utf-8")

    assert "overflow: hidden" in css
    assert "translateY(calc(-100% + 240px))" in css


def test_github_links_operate_correctly() -> None:
    content = Client().get("/portfolio/").content.decode()

    for project in FEATURED_PROJECTS:
        assert project.github_url in content
        assert 'rel="noopener noreferrer"' in content


def test_responsive_behavior_is_defined() -> None:
    css = PORTFOLIO_CSS.read_text(encoding="utf-8")

    assert "grid-template-columns: repeat(3, minmax(0, 1fr))" in css
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in css
    assert "@media" in css


def test_implementation_avoids_unnecessary_javascript() -> None:
    content = Client().get("/portfolio/").content.decode()

    assert "<script" not in content
