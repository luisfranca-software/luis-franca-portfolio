"""Integration tests for root routing (SPEC-001-REQ-001, SPEC-001-REQ-003).

The root path presents the Release 1 landing experience. Until the SPEC-001
Home phase is implemented, ``/`` renders the Portfolio module so the deployed
site never 404s at its entry point.
"""

from django.test import Client

from apps.portfolio.projects import FEATURED_PROJECTS


def test_root_path_returns_ok() -> None:
    response = Client().get("/")

    assert response.status_code == 200


def test_root_path_presents_release_1_projects() -> None:
    content = Client().get("/").content.decode()

    for project in FEATURED_PROJECTS:
        assert project.title in content
        assert project.github_url in content


def test_root_path_renders_no_live_demo_links() -> None:
    content = Client().get("/").content.decode()

    assert "Live demo" not in content
