"""Integration tests for responsive layout contracts (SPEC-001 section 7)."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_CSS = REPO_ROOT / "frontend" / "static" / "css" / "site.css"
HOME_CSS = REPO_ROOT / "frontend" / "static" / "css" / "home.css"
PORTFOLIO_CSS = REPO_ROOT / "frontend" / "static" / "css" / "portfolio.css"
SITE_JS = REPO_ROOT / "frontend" / "static" / "js" / "site.js"


def test_site_css_defines_mobile_breakpoint() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert "@media (max-width: 847px)" in css


def test_site_css_defines_tablet_breakpoint() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert "@media (min-width: 640px)" in css


def test_home_hero_stacks_on_mobile() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert ".home-hero {" in css
    assert "grid-template-columns: 1fr" in css


def test_home_hero_side_by_side_on_desktop() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "@media (min-width: 60.4375rem)" in css
    assert ".home-hero {" in css


def test_home_profile_photo_constrained_to_viewport() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert ".home-hero__visual .profile-photo {" in css
    assert "width: 100%" in css
    assert "height: auto" in css


def test_home_hero_wide_rule_does_not_force_reference_width_overflow() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")
    wide_rule = css.split("@media (min-width: 1200px)", 1)[1]

    assert "minmax(32rem, 1.1fr)" not in wide_rule
    assert "minmax(29rem, 0.9fr)" not in wide_rule


def test_images_globally_constrained_to_viewport() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert "img," in css
    assert "max-width: 100%" in css


def test_long_text_is_allowed_to_wrap() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert "overflow-wrap: break-word" in css


def test_navigation_accepts_narrow_viewports() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert ".site-nav {" in css
    assert "min-width: 0" in css
    assert ".site-nav__brand {" in css
    assert "flex-shrink: 0" in css


def test_skills_grid_is_responsive() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert ".skills-grid {" in css
    assert "grid-template-columns: 1fr" in css
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in css


def test_portfolio_grid_is_responsive() -> None:
    css = PORTFOLIO_CSS.read_text(encoding="utf-8")

    assert ".project-grid {" in css
    assert "grid-template-columns: 1fr" in css
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in css
    assert "grid-template-columns: repeat(3, minmax(0, 1fr))" in css


def test_homepage_styles_have_an_explicit_scope() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert ".site-main--homepage" in css
    assert ".homepage {" in css
    assert ".homepage__container" in css


def test_homepage_container_defines_approved_max_width() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "--homepage-content-max: 1344px" in css
    assert "calc(100% - (2 * var(--homepage-gutter)))" in css


def test_homepage_gutter_expression_covers_reference_geometry() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "2.9411764706vw + 9.4117647059px" in css
    assert "6.25vw - 16px" in css
    assert "clamp(32px, calc(6.25vw - 16px), 48px)" in css


def test_homepage_foundation_does_not_mask_horizontal_overflow() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "overflow-x: hidden" not in css
    assert "overflow-x:hidden" not in css


def test_homepage_foundation_does_not_copy_figma_page_heights() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    for prohibited_height in ("6960px", "5416px", "4428px", "2604px"):
        assert prohibited_height not in css


def test_homepage_foundation_records_approved_asset_authority() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "profile/luis-franca-transparent-02.png" in css
    assert "background/homepage-background-desktop-02.png" in css
    assert "profile/luis-franca-transparent.png" not in css
    assert "background/homepage-background-desktop.png" not in css


def test_header_preserves_sticky_runtime_contract() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")
    header_rule = css.split(".site-header {", maxsplit=1)[1].split("}", maxsplit=1)[0]

    assert "position: sticky" in header_rule
    assert "top: 0" in header_rule
    assert "z-index: 30" in header_rule


def test_header_interactive_targets_define_minimum_size() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert "min-width: 44px" in css
    assert css.count("min-height: 44px") >= 2


def test_compact_navigation_script_completes_disclosure_behavior() -> None:
    script = SITE_JS.read_text(encoding="utf-8")

    assert 'event.key === "Escape"' in script
    assert "toggle.focus()" in script
    assert 'toggle.setAttribute("aria-expanded", "false")' in script
    assert 'menu.querySelectorAll(".site-nav__link")' in script
    assert 'window.matchMedia("(min-width: 53rem)")' in script
    assert "FIT-HDR-001's validated 848px" in script


def test_homepage_anchor_targets_account_for_sticky_header() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")

    assert ".homepage__section[id]" in css
    assert "scroll-margin-top: 5rem" in css


def test_legacy_floating_whatsapp_css_is_removed() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert ".whatsapp-button" not in css
