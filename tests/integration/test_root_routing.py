"""Integration tests for root routing (SPEC-001-REQ-001, SPEC-001-REQ-003).

The root path now serves the SPEC-001 Home page. The dedicated Portfolio
section remains available at /portfolio/ (SPEC-001-REQ-007).
"""

from django.test import Client


def test_root_path_returns_ok() -> None:
    response = Client().get("/")

    assert response.status_code == 200


def test_root_path_presents_home_identity() -> None:
    content = Client().get("/").content.decode()

    assert "Luís França" in content
    assert "Luís Eduardo Carvalho França" in content
    assert "Software Engineer" in content
    assert "Python Backend Engineer" in content
    assert "AI/LLM Engineer" in content
    assert "Let&#x27;s Talk" in content


def test_root_path_includes_professional_photo() -> None:
    content = Client().get("/").content.decode()

    assert "profile-photo" in content
    assert "images/profile/luis-franca" in content


def test_portfolio_section_remains_available_at_dedicated_path() -> None:
    from apps.portfolio.projects import FEATURED_PROJECTS

    response = Client().get("/portfolio/")
    content = response.content.decode()

    assert response.status_code == 200
    for project in FEATURED_PROJECTS:
        assert project.title in content
