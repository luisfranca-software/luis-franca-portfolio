"""Final visual-hardening contracts for SDD-RWD-001 Block 14."""

import json
from pathlib import Path

from django.test import Client

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_CSS = REPO_ROOT / "frontend/static/css/home.css"
VISUAL_EVIDENCE = REPO_ROOT / "artifacts/responsive-visual/block14/block14-visual-validation.json"
SWEEP_EVIDENCE = REPO_ROOT / "artifacts/responsive-visual/block14/block14-full-width-sweep.json"


def test_hero_background_uses_approved_asset_and_continuity_contract() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")
    background = css.split(".homepage__technology-background {", 1)[1].split("}", 1)[0]

    assert "homepage-background-desktop-02.png" in background
    assert "background-position: top left" in background
    assert "background-size: 100vw auto" in background
    assert "background-repeat: repeat-y" in background
    assert "cover" not in background
    assert "no-repeat" not in background
    assert "position: absolute" in background
    assert "933px" not in background


def test_footer_has_local_clearance_for_fixed_ai_launcher() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")
    footer = css.split(".site-footer--homepage {", 1)[1].split("}", 1)[0]
    ai = css.split(".home-ai-rag {", 1)[1].split("}", 1)[0]

    assert "calc(clamp(2rem, 6vw, 3rem) + 3.5rem)" in footer
    assert "position: fixed" in ai
    assert "pointer-events: none" not in ai
    assert "padding-bottom" not in css.split(".homepage {", 1)[1].split("}", 1)[0]


def test_homepage_uses_approved_logo_without_changing_other_route_brand() -> None:
    home = Client().get("/").content.decode()
    about = Client().get("/about/").content.decode()
    home_nav = home.split('<nav class="site-nav"', 1)[1].split("</nav>", 1)[0]
    about_nav = about.split('<nav class="site-nav"', 1)[1].split("</nav>", 1)[0]

    assert 'class="brand-logo"' in home_nav
    assert 'loading="eager"' in home_nav
    assert 'class="site-nav__brand-name">Luís França' not in home_nav
    assert 'class="site-nav__brand-name">Luís França' in about_nav


def test_reference_and_interpolation_visual_evidence_is_collision_free() -> None:
    evidence = json.loads(VISUAL_EVIDENCE.read_text(encoding="utf-8"))

    assert evidence["reference_widths"] == [360, 768, 1024, 1440]
    assert evidence["interpolation_widths"] == [390, 480, 640, 820, 900, 1100, 1280]
    for locale in evidence["locales"]:
        assert set(locale["widths"]) == {
            "360",
            "390",
            "480",
            "640",
            "768",
            "820",
            "900",
            "1024",
            "1100",
            "1280",
            "1440",
        }
        for width, result in locale["widths"].items():
            assert result["overflow"] == {"page": False, "selectors": []}
            assert all(not words for words in result["broken_words"].values())
            assert not any(result["footer_target_collisions"].values())
            if result["reference"]:
                screenshot = REPO_ROOT / result["screenshot"]
                assert screenshot.is_file(), width


def test_final_sweep_preserves_every_fit_and_has_no_ai_collision() -> None:
    evidence = json.loads(SWEEP_EVIDENCE.read_text(encoding="utf-8"))

    for locale in evidence["locales"]:
        assert locale["sweep"]["page_overflow_widths"] == []
        assert all(
            transition["state"] == "FIT-VALIDATED" for transition in locale["transitions"].values()
        )
        assert all(
            not any(collisions.values())
            for collisions in locale["ai_rag_collision_observations"].values()
        )
