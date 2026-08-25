"""Structural contracts for SDD-RWD-001 Block 4 Homepage Hero."""

from pathlib import Path

from django.test import Client

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_CSS = REPO_ROOT / "frontend" / "static" / "css" / "home.css"
SITE_CSS = REPO_ROOT / "frontend" / "static" / "css" / "site.css"


def _home_content() -> str:
    return Client().get("/").content.decode()


def test_approved_asset_authorities_are_rendered_exclusively() -> None:
    content = _home_content()
    css = HOME_CSS.read_text(encoding="utf-8")

    assert "luis-franca-transparent-02.png" in content
    assert "homepage-background-desktop-02.png" in css
    assert "luis-franca-transparent.png" not in content
    assert 'homepage-background-desktop.png")' not in css


def test_copy_precedes_single_visual_region_in_one_hero_dom() -> None:
    content = _home_content()
    hero = content[content.index('<section class="home-hero') : content.index("</section>")]

    assert hero.count('class="home-hero__copy"') == 1
    assert hero.count('class="home-hero__visual"') == 1
    assert hero.index('class="home-hero__copy"') < hero.index('class="home-hero__visual"')
    assert content.count("<h1") == 1


def test_portrait_and_decorative_technology_accessibility_contract() -> None:
    content = _home_content()

    assert 'alt="Professional photograph of Luís Eduardo Carvalho França"' in content
    assert 'class="home-hero__ide" aria-hidden="true"' in content
    assert 'class="home-hero__explorer" aria-hidden="true"' in content
    assert 'class="home-hero__atmosphere" aria-hidden="true"' in content
    assert 'class="home-hero__gutter" aria-hidden="true"' in content
    assert 'class="home-hero__portrait-rim" aria-hidden="true"' in content


def test_portrait_alt_text_is_translated_in_pt_br() -> None:
    client = Client()
    client.cookies["django_language"] = "pt-br"

    assert "Fotografia profissional de Luís Eduardo Carvalho França" in (
        client.get("/").content.decode()
    )


def test_hero_actions_keep_authoritative_destinations(contact_links: dict[str, str]) -> None:
    content = _home_content()

    assert 'href="/contact/"' in content
    assert f'href="{contact_links["linkedin"]}"' in content
    assert f'href="{contact_links["github"]}"' in content


def test_technology_layers_and_occlusion_order_exist() -> None:
    content = _home_content()
    markers = (
        'class="home-hero__atmosphere"',
        'class="home-hero__gutter"',
        'class="home-hero__ide"',
        'class="home-hero__explorer"',
        'class="home-hero__portrait-rim"',
        'class="profile-photo"',
    )

    assert [content.index(marker) for marker in markers] == sorted(
        content.index(marker) for marker in markers
    )


def test_technology_layers_have_independent_trace_authority() -> None:
    content = _home_content()

    trace_ids = (
        "IMG-02", "HERO-07", "HERO-07A", "HERO-07B",
        "HERO-08", "HERO-08A", "HERO-08B", "IMG-00",
    )
    for trace_id in trace_ids:
        assert content.count(f'data-trace-id="{trace_id}"') == 1


def test_hero_uses_local_coordinates_without_global_overflow_masking() -> None:
    home_css = HOME_CSS.read_text(encoding="utf-8")
    site_css = SITE_CSS.read_text(encoding="utf-8")
    visual_rule = home_css.split(".home-hero__visual {", 1)[1].split("}", 1)[0]

    assert "position: relative" in visual_rule
    assert "PROVISIONAL IMPLEMENTATION THRESHOLD" not in home_css
    assert "FIT-HERO-001 — validated at 967 CSS px" in home_css
    assert "overflow-x: hidden" not in home_css + site_css
    for prohibited_height in ("6960px", "5416px", "4428px", "2604px"):
        assert prohibited_height not in home_css


def test_non_homepage_route_does_not_load_homepage_styles_or_background() -> None:
    content = Client().get("/about/").content.decode()

    assert 'href="/static/css/home.css"' not in content
    assert 'class="homepage"' not in content


def test_anomalous_portrait_rim_effect_is_not_rendered() -> None:
    """HERO-09A stays traceable while its rejected CSS geometry is disabled."""
    content = _home_content()
    css = HOME_CSS.read_text(encoding="utf-8")

    assert 'data-trace-id="HERO-09A"' in content
    rule = css.split(".home-hero__portrait-rim {", 1)[1].split("}", 1)[0]
    assert "display: none" in rule
    assert "luis-franca-transparent-02.png" in content
    assert 'class="home-hero__ide"' in content
    assert 'class="home-hero__explorer"' in content


def test_desktop_intermediate_titles_use_scoped_fluid_locale_fit() -> None:
    css = HOME_CSS.read_text(encoding="utf-8")
    scope = css.split(
        "@media (min-width: 967px) and (max-width: 1199px) {", 1
    )[1].split("@media (min-width: 1200px)", 1)[0]

    assert "grid-template-columns:" in scope
    assert "clamp(416px" in scope
    assert "calc(82.14666193vw - 425.18181818px)" in scope
    assert "font-size: clamp(33px" in scope
    assert ".homepage:lang(pt-BR) .home-hero__titles" in scope
    assert "font-size: clamp(30px" in scope
    assert "48px" in scope
    assert "transform" not in scope
