"""Contracts for the nonfunctional SDD-RWD-001 Block 10 AI/RAG visual."""

from pathlib import Path

from django.test import Client

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_CSS = REPO_ROOT / "frontend" / "static" / "css" / "home.css"
SITE_JS = REPO_ROOT / "frontend" / "static" / "js" / "site.js"


def _home_content() -> str:
    return Client().get("/").content.decode()


def test_reserved_visual_renders_once_only_on_homepage() -> None:
    content = _home_content()

    assert content.count('class="home-ai-rag" aria-hidden="true"') == 1
    for path in ("/about/", "/skills/", "/experience/", "/portfolio/", "/contact/"):
        assert "home-ai-rag" not in Client().get(path).content.decode()


def test_reserved_visual_is_neutral_and_noninteractive() -> None:
    content = _home_content()
    start = content.index('class="home-ai-rag"')
    visual = content[content.rfind("<", 0, start) : content.index("</div>", start)]

    assert visual.startswith("<div")
    assert visual.count("Juju IA") == 1
    assert "Jujuju AI" not in visual
    assert "Juju AI" not in visual
    assert "Ask AI / RAG" not in visual
    assert "Explore engineering context" not in visual
    assert "Pergunte à IA / RAG" not in visual
    assert "Explore o contexto de engenharia" not in visual
    for prohibited in (
        "<a ",
        "<button",
        "href=",
        "tabindex=",
        "role=",
        "aria-expanded=",
        "aria-controls=",
        "aria-haspopup=",
        "onclick=",
    ):
        assert prohibited not in visual


def test_fixed_gutter_safe_area_and_layer_contracts_exist() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")
    rule = css.split(".home-ai-rag {", 1)[1].split("}", 1)[0]

    assert "position: fixed" in rule
    assert "z-index: 20" in rule
    assert "right: max(var(--homepage-gutter), env(safe-area-inset-right, 0px))" in rule
    assert "bottom: max(var(--homepage-gutter), env(safe-area-inset-bottom, 0px))" in rule
    assert "pointer-events: none" in rule
    normal_flow_rule = css.split(
        ".homepage > :not(.homepage__technology-background):not(.home-ai-rag) {",
        1,
    )[1].split("}", 1)[0]
    assert "position: relative" in normal_flow_rule
    assert "z-index: 30" in (
        REPO_ROOT / "frontend/static/css/site.css"
    ).read_text(encoding="utf-8")


def test_no_ai_rag_runtime_or_release_two_scaffolding_exists() -> None:
    script = SITE_JS.read_text(encoding="utf-8").lower()

    assert "ai-rag" not in script
    assert "ai_rag" not in script
    assert "fetch(" not in script
    assert "websocket" not in script
    assert "eventsource" not in script


def test_product_name_is_locale_invariant() -> None:
    english = Client(HTTP_ACCEPT_LANGUAGE="en").get("/").content.decode()
    portuguese = Client(HTTP_ACCEPT_LANGUAGE="pt-br").get("/").content.decode()

    assert english.count("Juju IA") == 1
    assert portuguese.count("Juju IA") == 1
    assert "Jujuju AI" not in english + portuguese
    assert "Juju AI" not in english + portuguese


def test_reserved_visual_is_independent_of_footer_and_fit_states() -> None:
    content = _home_content()
    footer_start = content.index('<footer class="site-footer')
    visual_start = content.index('class="home-ai-rag"')
    css = HOME_CSS.read_text(encoding="utf-8")

    assert visual_start < footer_start
    assert "home-ai-rag" not in content[footer_start:]
    assert "FIT-" not in css.split(".home-ai-rag {", 1)[1].split("}", 1)[0]
    assert "overflow-x: hidden" not in css
    assert ".site-footer--homepage { padding: 32px var(--homepage-gutter, 20px) 104px; }" in css
