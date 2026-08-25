"""Structural contracts for SDD-RWD-001 Block 6 selected project work."""

from pathlib import Path
from typing import Any

from django.test import Client

from apps.portfolio.projects import FEATURED_PROJECTS

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_CSS = REPO_ROOT / "frontend" / "static" / "css" / "home.css"


def _projects_response() -> tuple[Any, str]:
    response = Client().get("/")
    content = response.content.decode()
    start = content.index('id="projects"')
    return response, content[start : content.index("</section>", start)]


def test_projects_preserve_semantics_canonical_authority_and_order() -> None:
    response, section = _projects_response()

    assert section.count('id="projects"') == 1
    assert section.count('<h2 id="projects-heading">') == 1
    assert section.count('class="home-project"') == len(FEATURED_PROJECTS) == 3
    assert section.count("<h3>") == 3
    assert response.context["featured_projects"] is FEATURED_PROJECTS
    markers = [f'data-home-project="{project.slug}"' for project in FEATURED_PROJECTS]
    assert [section.index(marker) for marker in markers] == sorted(
        section.index(marker) for marker in markers
    )


def test_home_projects_render_canonical_content_assets_and_destinations() -> None:
    _response, section = _projects_response()

    for project in FEATURED_PROJECTS:
        assert project.title in section
        assert project.summary in section
        assert project.screenshot_master in section
        assert project.github_url in section
        for path, _width in project.webp_variants:
            assert path in section
        for technology in project.technologies:
            assert technology in section


def test_project_images_and_links_are_accessible() -> None:
    _response, section = _projects_response()

    assert section.count('alt="Screenshot of ') == 3
    assert section.count('rel="noopener noreferrer"') == 3
    assert section.count("source on GitHub") == 3
    for prohibited in ("<button", "tabindex=", 'role="button"', "onclick="):
        assert prohibited not in section


def test_project_accessibility_label_is_translated_in_pt_br() -> None:
    content = Client(HTTP_ACCEPT_LANGUAGE="pt-br").get("/").content.decode()
    start = content.index('id="projects"')
    section = content[start : content.index("</section>", start)]

    assert section.count('aria-label="Tecnologias"') == 3


def test_project_layout_represents_reference_modes_without_reordering() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "FIT-PRJ-001 — validated shared 896px" in css
    assert "FIT-PRJ-002 — validated shared 1200px" in css
    assert "grid-template-columns: minmax(0, 1fr)" in css
    assert "grid-template-columns: repeat(4, minmax(0, 1fr))" in css
    assert "grid-column: 2 / span 2" in css
    assert "grid-template-columns: repeat(3, minmax(0, 1fr))" in css
    project_css = css[css.index("/* Selected Engineering Work") :]
    assert "\n    order:" not in project_css
    assert "overflow-x: hidden" not in css


def test_home_project_styles_do_not_leak_to_portfolio() -> None:
    content = Client().get("/portfolio/").content.decode()

    assert 'href="/static/css/home.css"' not in content
    assert "home-project" not in content
    assert 'href="/static/css/portfolio.css"' in content


def test_block_six_preserves_remaining_future_boundary() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert ".home-ai-rag" in css
