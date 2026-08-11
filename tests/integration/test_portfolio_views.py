"""Integration tests for the Portfolio views and URLs (SPEC-003).

Verifies the dedicated Portfolio section (SPEC-003-REQ-001), the presentation
of the three featured projects (SPEC-003-REQ-002), reusable project cards
(SPEC-003-REQ-003) and the card content contract (SPEC-003-REQ-004).
"""

from django.test import Client

from apps.portfolio.projects import FEATURED_PROJECTS


def test_portfolio_page_renders() -> None:
    response = Client().get("/portfolio/")

    assert response.status_code == 200


def test_portfolio_page_presents_all_featured_projects() -> None:
    response = Client().get("/portfolio/")
    content = response.content.decode()

    for project in FEATURED_PROJECTS:
        assert project.title in content
        assert project.summary in content
        assert project.github_url in content


def test_portfolio_page_renders_reusable_card_per_project() -> None:
    content = Client().get("/portfolio/").content.decode()

    assert content.count("<article") == len(FEATURED_PROJECTS)


def test_portfolio_page_shows_technology_badges() -> None:
    content = Client().get("/portfolio/").content.decode()

    for project in FEATURED_PROJECTS:
        for tech in project.technologies:
            assert tech in content


def test_demo_links_rendered_when_available() -> None:
    content = Client().get("/portfolio/").content.decode()

    with_demo = sum(1 for project in FEATURED_PROJECTS if project.demo_url)
    assert content.count("Live demo") == with_demo
    for project in FEATURED_PROJECTS:
        if project.demo_url:
            assert project.demo_url in content


def test_screenshots_use_responsive_delivery() -> None:
    content = Client().get("/portfolio/").content.decode()

    for project in FEATURED_PROJECTS:
        assert project.screenshot_master in content
        for path, _width in project.webp_variants:
            assert path in content


def test_portfolio_page_loads_module_stylesheet() -> None:
    content = Client().get("/portfolio/").content.decode()

    assert "css/portfolio.css" in content
