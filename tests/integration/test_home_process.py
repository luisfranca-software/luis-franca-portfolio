"""Structural contracts for SDD-RWD-001 Block 7 Process section."""

from pathlib import Path
from typing import Any

from django.test import Client

from apps.home.content import PROCESS_STEPS

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_CSS = REPO_ROOT / "frontend" / "static" / "css" / "home.css"


def _process_response(language: str = "en") -> tuple[Any, str]:
    response = Client(HTTP_ACCEPT_LANGUAGE=language).get("/")
    content = response.content.decode()
    start = content.index('id="process"')
    return response, content[start : content.index("</section>", start)]


def test_process_preserves_semantics_authoritative_source_and_order() -> None:
    response, section = _process_response()

    assert section.count('id="process"') == 1
    assert section.count('<h2 id="process-heading">') == 1
    assert section.count('class="home-process__step"') == len(PROCESS_STEPS) == 7
    assert section.count("<h3>") == 7
    assert response.context["process_steps"] is PROCESS_STEPS
    markers = [f'data-process-step="{step.slug}"' for step in PROCESS_STEPS]
    assert [section.index(marker) for marker in markers] == sorted(
        section.index(marker) for marker in markers
    )
    assert section.rindex('data-process-step="validation"') > section.rindex(
        'data-process-step="deployment"'
    )


def test_process_connectors_and_steps_are_noninteractive() -> None:
    _response, section = _process_response()

    assert section.count('class="home-process__marker" aria-hidden="true"') == 7
    for prohibited in ("<button", "<a ", "tabindex=", 'role="button"', "onclick="):
        assert prohibited not in section


def test_process_layout_represents_all_modes_and_centering_contracts() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "FIT-PRC-001 — validated shared 640px" in css
    assert "FIT-PRC-002 — validated shared 896px" in css
    assert "FIT-PRC-003 — validated shared 1200px" in css
    assert "grid-template-columns: minmax(0, 1fr)" in css
    assert "grid-template-columns: repeat(4, minmax(0, 1fr))" in css
    assert "grid-column: 2 / span 2" in css
    assert "grid-template-columns: repeat(6, minmax(0, 1fr))" in css
    assert "grid-column: 3 / span 2" in css
    assert "grid-template-columns: repeat(7, minmax(0, 1fr))" in css
    process_css = css[css.index("/* Process — Block 7") :]
    assert "\n    order:" not in process_css
    assert "overflow-x: hidden" not in css
    step_rule = process_css.split(".home-process__step {", 1)[1].split("}", 1)[0]
    assert "height:" not in step_rule


def test_process_renders_english_and_portuguese_without_duplication() -> None:
    _response, english = _process_response()
    _response, portuguese = _process_response("pt-br")

    assert "Requirements" in english
    assert "Validation" in english
    assert "Requisitos" in portuguese
    assert "Validação" in portuguese
    assert portuguese.count('class="home-process__step"') == 7


def test_process_styles_are_homepage_only() -> None:
    content = Client().get("/about/").content.decode()

    assert 'href="/static/css/home.css"' not in content
    assert "home-process" not in content


def test_block_seven_does_not_style_future_sections() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert ".home-ai-rag" in css
