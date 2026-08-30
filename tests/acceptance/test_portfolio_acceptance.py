"""Acceptance tests for SPEC-003 — Portfolio & Projects (section 12).

Acceptance is based on objective evidence produced through the automated test
suite, aligned with TST-001 and the SPEC-003 acceptance criteria. Tests
validate the approved Release 1 data (order, titles, summaries, technologies,
GitHub URLs), the zero-demo-dataset behavior, and the absence of placeholder
URLs in tracked implementation files.
"""

from pathlib import Path

from django.test import Client

from apps.portfolio.projects import FEATURED_PROJECTS

REPO_ROOT = Path(__file__).resolve().parents[2]
PORTFOLIO_CSS = REPO_ROOT / "frontend" / "static" / "css" / "portfolio.css"

SKIPPED_DIRS = {
    ".git",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "staticfiles",
    "media",
}
SKIPPED_SUFFIXES = {".png", ".webp", ".jpg", ".jpeg", ".gif", ".ico", ".mo", ".pyc"}


def _tracked_implementation_files():
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIPPED_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        if path.suffix.lower() in SKIPPED_SUFFIXES:
            continue
        yield path


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


def test_approved_titles_and_summaries_are_rendered() -> None:
    content = Client().get("/portfolio/").content.decode()

    for project in FEATURED_PROJECTS:
        assert project.title in content
        assert project.summary in content


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


def test_release_1_renders_no_live_demo_links() -> None:
    content = Client().get("/portfolio/").content.decode()

    assert "Live demo" not in content
    assert "class=\"project-card__link--demo\"" not in content
    for project in FEATURED_PROJECTS:
        assert project.demo_url is None


def test_example_com_is_only_the_authorized_contact_email_placeholder() -> None:
    placeholder_domain = "example." + "com"
    authorized_files = {
        "backend/apps/contact/forms.py",
        "backend/locale/pt_BR/LC_MESSAGES/django.po",
        "tests/integration/test_contact_i18n.py",
    }
    offenders = []
    for path in _tracked_implementation_files():
        relative_path = str(path.relative_to(REPO_ROOT))
        if relative_path in authorized_files or relative_path.startswith("artifacts/"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if placeholder_domain in text:
            offenders.append(relative_path)
    assert offenders == []


def test_no_forbidden_github_owner_in_implementation_files() -> None:
    forbidden_owner = "https://github.com/" + "luis-franca/"
    offenders = []
    for path in _tracked_implementation_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if forbidden_owner in text:
            offenders.append(str(path))
    assert offenders == []


def test_responsive_behavior_is_defined() -> None:
    css = PORTFOLIO_CSS.read_text(encoding="utf-8")

    assert "grid-template-columns: repeat(3, minmax(0, 1fr))" in css
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in css
    assert "@media" in css


def test_portfolio_does_not_add_module_specific_javascript() -> None:
    content = Client().get("/portfolio/").content.decode()

    # The only script is the shared site.js used by global navigation
    # (SPEC-001-REQ-002); the Portfolio module itself adds no scripts.
    assert "<script" in content
    assert content.count("<script") == 1
    assert "js/site.js" in content
    assert "portfolio.js" not in content
