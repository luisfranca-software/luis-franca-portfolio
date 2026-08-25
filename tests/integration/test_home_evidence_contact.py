"""Structural contracts for SDD-RWD-001 Block 8 Evidence and Contact CTA."""

from pathlib import Path
from typing import Any

from django.test import Client

from apps.home.content import EVIDENCE_THEMES

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_CSS = REPO_ROOT / "frontend" / "static" / "css" / "home.css"


def _home_response(language: str = "en") -> tuple[Any, str]:
    response = Client(HTTP_ACCEPT_LANGUAGE=language).get("/")
    return response, response.content.decode()


def _section(content: str, section_id: str) -> str:
    start = content.index(f'id="{section_id}"')
    return content[start : content.index("</section>", start)]


def test_evidence_preserves_semantics_authoritative_source_and_order() -> None:
    response, content = _home_response()
    evidence = _section(content, "evidence")

    assert content.count('id="evidence"') == 1
    assert evidence.count('<h2 id="evidence-heading">') == 1
    assert evidence.count('class="home-evidence__item"') == len(EVIDENCE_THEMES) == 4
    assert evidence.count("<h3>") == 4
    assert response.context["evidence_themes"] is EVIDENCE_THEMES
    markers = [f'data-evidence-theme="{theme.slug}"' for theme in EVIDENCE_THEMES]
    assert [evidence.index(marker) for marker in markers] == sorted(
        evidence.index(marker) for marker in markers
    )


def test_evidence_is_noninteractive_and_uses_approved_descriptions() -> None:
    _response, content = _home_response()
    evidence = _section(content, "evidence")

    assert 'class="home-evidence__icon"' not in evidence
    assert evidence.count("<p>") == 4
    for prohibited in ("<button", "<a ", "tabindex=", 'role="button"', "onclick="):
        assert prohibited not in evidence


def test_contact_is_separate_and_uses_existing_route_once() -> None:
    _response, content = _home_response()
    evidence = _section(content, "evidence")
    contact = _section(content, "contact")

    assert content.count('id="contact"') == 1
    assert contact.count('id="contact-heading"') == 1
    assert contact.count('class="home-contact__action button button--primary"') == 1
    assert contact.count('href="/contact/"') == 1
    assert evidence not in contact


def test_evidence_contact_layout_and_fit_contracts_are_validated() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "FIT-EVD-001 — validated shared 640px" in css
    assert "FIT-EVD-002 and FIT-EVD-003 — validated shared 1200px" in css
    assert "grid-template-columns: minmax(0, 1fr)" in css
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in css
    assert "grid-template-columns: repeat(4, minmax(0, 1fr))" in css
    assert "grid-template-columns: minmax(0, 2fr) minmax(20rem, 1fr)" in css
    assert "overflow-x: hidden" not in css


def test_evidence_and_contact_render_in_english_and_portuguese() -> None:
    _response, english = _home_response()
    _response, portuguese = _home_response("pt-br")

    assert "Professional Evidence" in english
    assert "Open to challenging software engineering work" in english
    assert "Evidências Profissionais" in portuguese
    assert "trabalho desafiador de engenharia de software" in portuguese
    assert "Entre em contato" in portuguese


def test_evidence_contact_styles_are_homepage_only() -> None:
    content = Client().get("/contact/").content.decode()

    assert 'href="/static/css/home.css"' not in content
    assert "home-evidence-contact" not in content


def test_reserved_visual_remains_outside_evidence_contact_semantics() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert ".home-ai-rag" in css
