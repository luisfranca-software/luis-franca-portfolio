"""Structural contracts for SDD-RWD-001 Block 9 Homepage Footer."""

import re
from pathlib import Path

from django.test import Client

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_CSS = REPO_ROOT / "frontend" / "static" / "css" / "home.css"


def _footer(path: str = "/", language: str = "en") -> str:
    content = Client(HTTP_ACCEPT_LANGUAGE=language).get(path).content.decode()
    start = content.index('<footer class="site-footer')
    return content[start : content.index("</footer>", start)]


def test_homepage_footer_has_one_landmark_and_approved_semantic_order() -> None:
    footer = _footer()

    assert footer.count("<footer") == 1
    assert 'class="site-footer site-footer--homepage"' in footer
    markers = (
        'class="homepage-footer__brand"',
        'class="homepage-footer__copyright"',
        'class="homepage-footer__tagline"',
        'class="homepage-footer__nav"',
        'class="homepage-footer__social"',
    )
    assert [footer.index(marker) for marker in markers] == sorted(
        footer.index(marker) for marker in markers
    )
    assert "Engineering with evidence." in footer


def test_homepage_footer_preserves_authoritative_destinations(contact_links) -> None:
    footer = _footer()

    assert 'href="#projects"' in footer
    assert 'href="#contact"' in footer
    assert contact_links["linkedin"] in footer
    assert contact_links["github"] in footer
    assert contact_links["resume"] not in footer
    assert footer.count('rel="noopener noreferrer"') == 2


def test_homepage_footer_year_is_generated_at_render_time() -> None:
    footer = _footer()
    template = REPO_ROOT / "frontend/templates/includes/homepage-footer.html"

    assert re.search(r"© \d{4} Luís França", footer)
    assert '{% now "Y" %}' in template.read_text(encoding="utf-8")


def test_homepage_footer_represents_stacked_and_horizontal_modes() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "FIT-FTR-001 — validated shared 640px" in css
    assert ".site-footer--homepage" in css
    assert "grid-template-columns: minmax(0, 1fr)" in css
    assert "auto minmax(8rem, 1fr) minmax(8rem, 1fr) auto auto" in css
    footer_rule = css.split(".site-footer--homepage {", 1)[1].split("}", 1)[0]
    assert "height: 336px" not in footer_rule
    assert "overflow-x: hidden" not in css


def test_homepage_footer_is_translated_and_links_are_accessible() -> None:
    footer = _footer(language="pt-br")

    assert "Engenharia com evidências." in footer
    assert 'aria-label="Navegação do rodapé"' in footer
    assert "min-height: 44px" in HOME_CSS.read_text(encoding="utf-8")


def test_non_homepage_footer_keeps_release_one_content(contact_links) -> None:
    footer = _footer("/about/")

    assert "site-footer--homepage" not in footer
    for label in ("Navigation", "Home", "About", "Skills", "Experience", "Portfolio"):
        assert label in footer
    assert contact_links["linkedin"] in footer
    assert contact_links["github"] in footer
    assert contact_links["resume"] in footer


def test_ai_rag_reserved_visual_remains_outside_footer_flow() -> None:
    assert "home-ai-rag" not in _footer().lower()
    assert ".home-ai-rag" in HOME_CSS.read_text(encoding="utf-8")
