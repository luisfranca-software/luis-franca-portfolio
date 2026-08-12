"""Integration tests for responsive layout contracts (SPEC-001 section 7)."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_CSS = REPO_ROOT / "frontend" / "static" / "css" / "site.css"
PORTFOLIO_CSS = REPO_ROOT / "frontend" / "static" / "css" / "portfolio.css"


def test_site_css_defines_mobile_breakpoint() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert "@media (max-width: 768px)" in css


def test_site_css_defines_tablet_breakpoint() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert "@media (min-width: 640px)" in css


def test_home_hero_stacks_on_mobile() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert ".home-hero {" in css
    assert "grid-template-columns: 1fr" in css


def test_home_hero_side_by_side_on_desktop() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    assert "@media (min-width: 768px)" in css
    assert ".home-hero {" in css


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
