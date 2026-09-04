"""Contracts for the SDD-RWD-001 Block 10 AI/RAG interactive launcher.

Governing documents: ADR-007 §20, SPEC-005 §37.
The visual has evolved from a decorative reserved element into the functional,
accessible IA Jujuju launcher.
"""

from pathlib import Path

from django.test import Client

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_CSS = REPO_ROOT / "frontend" / "static" / "css" / "home.css"
SITE_JS = REPO_ROOT / "frontend" / "static" / "js" / "site.js"


def _home_content() -> str:
    return Client().get("/").content.decode()


def test_launcher_renders_once_only_on_homepage() -> None:
    content = _home_content()

    assert content.count('class="home-ai-rag"') == 1
    for path in ("/about/", "/skills/", "/experience/", "/portfolio/", "/contact/"):
        assert "home-ai-rag" not in Client().get(path).content.decode()


def test_launcher_is_interactive_button() -> None:
    content = _home_content()
    start = content.index('class="home-ai-rag"')
    visual = content[content.rfind("<", 0, start) : content.index("</button>", start)]

    assert visual.startswith("<button")
    assert visual.count("IA Jujuju") == 2
    assert "Juju IA" not in visual
    assert "Jujuju AI" not in visual
    assert "Juju AI" not in visual
    assert "Ask AI / RAG" not in visual
    assert "Explore engineering context" not in visual
    assert "Pergunte \u00e0 IA / RAG" not in visual
    assert "Explore o contexto de engenharia" not in visual
    assert 'type="button"' in visual
    assert "aria-label=" in visual
    assert "aria-expanded=" in visual
    assert "aria-controls=" in visual
    assert "hx-get=" in visual
    assert "hx-target=" in visual
    assert "tabindex=" not in visual


def test_fixed_gutter_safe_area_and_layer_contracts_exist() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")
    rule = css.split(".home-ai-rag {", 1)[1].split("}", 1)[0]

    assert "position: fixed" in rule
    assert "z-index: 20" in rule
    assert "right: max(var(--homepage-gutter), env(safe-area-inset-right, 0px))" in rule
    assert "bottom: max(var(--homepage-gutter), env(safe-area-inset-bottom, 0px))" in rule
    child_layering_selector = (
        ".homepage > :not(.homepage__technology-background)"
        ":not(.home-ai-rag):not(.assistant-container) {"
    )
    normal_flow_rule = css.split(child_layering_selector, 1)[1].split("}", 1)[0]
    assert "position: relative" in normal_flow_rule
    assert ".assistant-container" not in normal_flow_rule
    assert "z-index: 30" in (REPO_ROOT / "frontend/static/css/site.css").read_text(encoding="utf-8")


def test_launcher_has_interactive_styles() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")
    rule = css.split(".home-ai-rag {", 1)[1].split("}", 1)[0]

    assert "cursor: pointer" in rule
    assert 'input:not([type="button"])' not in rule


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

    assert english.count("IA Jujuju") == 2
    assert portuguese.count("IA Jujuju") == 2
    assert "Juju IA" not in english + portuguese
    assert "Jujuju AI" not in english + portuguese
    assert "Juju AI" not in english + portuguese


def test_launcher_is_independent_of_footer_and_fit_states() -> None:
    content = _home_content()
    footer_start = content.index('<footer class="site-footer')
    visual_start = content.index('class="home-ai-rag"')
    css = HOME_CSS.read_text(encoding="utf-8")

    assert visual_start < footer_start
    assert "home-ai-rag" not in content[footer_start:]
    assert "FIT-" not in css.split(".home-ai-rag {", 1)[1].split("}", 1)[0]
    assert "overflow-x: hidden" not in css
    assert ".site-footer--homepage { padding: 32px var(--homepage-gutter, 20px) 104px; }" in css


def test_assistant_container_escapes_homepage_child_layering_rule() -> None:
    """Regression: .assistant-container must keep position: fixed / z-index: 40.

    The generic Homepage child-layering selector previously captured
    .assistant-container and overrode its fixed positioning, causing the panel
    to render in normal flow near the footer instead of floating.
    """
    css = HOME_CSS.read_text(encoding="utf-8")
    child_layering_selector = (
        ".homepage > :not(.homepage__technology-background)"
        ":not(.home-ai-rag):not(.assistant-container) {"
    )
    assert child_layering_selector in css

    child_layering_rule = css.split(child_layering_selector, 1)[1].split("}", 1)[0]
    assert "position: relative" in child_layering_rule
    assert ".assistant-container" not in child_layering_rule

    panel_rule = css.split(".assistant-container {", 1)[1].split("}", 1)[0]
    assert "position: fixed" in panel_rule
    assert "z-index: 40" in panel_rule


def test_mobile_assistant_overlay_contract_is_represented_in_markup_and_css() -> None:
    content = _home_content()
    css = HOME_CSS.read_text(encoding="utf-8")

    assert content.index("</div>\n\n<button") < content.index('class="home-ai-rag"')
    assert "body.assistant-open .home-ai-rag" in css
    panel_rule = css.split(".assistant-container {", 1)[1].split("}", 1)[0]
    assert "z-index: 40" in panel_rule
    assert "position: fixed" in panel_rule
    assert "top: max(0.75rem, env(safe-area-inset-top, 0px))" in css
    assert "100dvh" in css


def test_reduced_motion_and_assistant_motion_contracts_exist() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")
    script = (REPO_ROOT / "frontend" / "static" / "js" / "assistant.js").read_text(encoding="utf-8")

    assert ".assistant-message--enter" in css
    assert "@keyframes assistant-message-enter" in css
    assert ".assistant-message__word" in css
    assert "@media (prefers-reduced-motion: reduce)" in css
    assert 'matchMedia("(prefers-reduced-motion: reduce)")' in script
    assert "htmx:afterSwap" in script
