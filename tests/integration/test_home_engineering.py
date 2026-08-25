"""Structural contracts for SDD-RWD-001 Block 5 Engineering section."""

from pathlib import Path

from django.test import Client

from apps.home.content import ENGINEERING_CAPABILITIES

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_CSS = REPO_ROOT / "frontend" / "static" / "css" / "home.css"


def _engineering_fragment(content: str) -> str:
    marker = '<section\n  class="homepage__section homepage__container home-engineering"'
    start = content.index(marker)
    return content[start : content.index("</section>", start)]


def test_engineering_section_preserves_semantics_and_authoritative_order() -> None:
    response = Client().get("/")
    content = response.content.decode()
    section = _engineering_fragment(content)

    assert content.count('id="engineering"') == 1
    assert section.count('<h2 id="engineering-heading">') == 1
    assert section.count("<h3>") == len(ENGINEERING_CAPABILITIES) == 4
    assert response.context["engineering_capabilities"] is ENGINEERING_CAPABILITIES
    markers = [
        f'data-engineering-item="{capability.slug}"'
        for capability in ENGINEERING_CAPABILITIES
    ]
    assert [section.index(marker) for marker in markers] == sorted(
        section.index(marker) for marker in markers
    )


def test_engineering_cards_are_noninteractive_and_omit_unapproved_decoration() -> None:
    section = _engineering_fragment(Client().get("/").content.decode())

    assert 'class="home-engineering__icon"' not in section
    assert 'class="home-engineering__direction"' not in section
    for prohibited in ("<button", "tabindex=", 'role="menu"', "onclick="):
        assert prohibited not in section


def test_engineering_layout_contracts_are_validated_and_intrinsic() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "FIT-ENG-001 — validated shared 640px" in css
    assert "FIT-ENG-002 — validated shared 1200px" in css
    assert "PROVISIONAL IMPLEMENTATION THRESHOLD" not in css
    assert "grid-template-columns: minmax(0, 1fr)" in css
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in css
    assert "grid-template-columns: repeat(4, minmax(0, 1fr))" in css
    assert "overflow-x: hidden" not in css
    assert "height:" not in css.split(".home-engineering__item {", 1)[1].split("}", 1)[0]


def test_engineering_styles_are_homepage_only() -> None:
    content = Client().get("/about/").content.decode()

    assert 'href="/static/css/home.css"' not in content
    assert "home-engineering" not in content


def test_reserved_visual_does_not_change_engineering_scope() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert ".home-ai-rag" in css
