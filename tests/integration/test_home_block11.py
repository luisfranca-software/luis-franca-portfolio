"""Cross-cutting contracts for SDD-RWD-001 Block 11."""

from pathlib import Path

from django.test import Client

from apps.portfolio.projects import FEATURED_PROJECTS

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_CSS = REPO_ROOT / "frontend/static/css/home.css"
SITE_CSS = REPO_ROOT / "frontend/static/css/site.css"


def _home(language: str = "en") -> str:
    return Client(HTTP_ACCEPT_LANGUAGE=language).get("/").content.decode()


def test_homepage_landmarks_and_heading_hierarchy_remain_semantic() -> None:
    content = _home()

    assert content.count("<header") >= 1
    assert content.count("<nav") >= 1
    assert content.count('<main id="main-content"') == 1
    assert content.count("<footer") >= 1
    assert content.count("<h1") == 1
    assert content.count("<h2") == 5
    assert content.index("<h1") < content.index("<h2") < content.index("<h3")


def test_decorative_layers_and_reserved_visual_stay_out_of_tab_order() -> None:
    content = _home()

    for marker in (
        'home-hero__atmosphere" aria-hidden="true"',
        'home-hero__gutter" aria-hidden="true"',
        'home-hero__ide" aria-hidden="true"',
        'home-hero__explorer" aria-hidden="true"',
        'home-hero__portrait-rim" aria-hidden="true"',
    ):
        assert marker in content


def test_ai_rag_launcher_is_interactive_and_accessible() -> None:
    content = _home()

    start = content.index('class="home-ai-rag"')
    launcher = content[content.rfind("<", 0, start) : content.index("</button>", start)]

    assert launcher.startswith("<button")
    assert 'type="button"' in launcher
    assert "aria-label=" in launcher
    assert 'aria-expanded="false"' in launcher
    assert 'aria-controls="assistant-container"' in launcher
    assert "aria-hidden=" not in launcher.split('class="home-ai-rag"')[1].split(">", 1)[0]


def test_changed_header_controls_keep_target_and_focus_contracts() -> None:
    css = SITE_CSS.read_text(encoding="utf-8")

    brand = css.split(".site-nav__brand {", 1)[1].split("}", 1)[0]
    selector = css.split(".language-selector select {", 1)[1].split("}", 1)[0]
    assert "min-height: 44px" in brand
    assert "min-height: 44px" in selector
    assert ".site-nav__toggle:focus-visible" in css
    assert ".language-selector select:focus-visible" in css


def test_portuguese_homepage_translates_project_information_and_logo_name() -> None:
    content = _home("pt-br")

    assert "Plataforma web de nível empresarial" in content
    assert "Plataforma modular de inteligência cambial" in content
    assert "Aplicação RPA em Python" in content
    assert 'alt="Logotipo do Site Portfolio de Luís França"' in content
    for project in FEATURED_PROJECTS:
        assert project.summary not in content


def test_homepage_images_use_responsive_delivery_and_reserve_space() -> None:
    content = _home()

    for width in (480, 768, 1024):
        assert f"luis-franca-transparent-02-{width}.webp" in content
    assert 'width="1385"' in content
    assert 'height="1136"' in content
    assert 'fetchpriority="high"' in content
    portrait = content.split('class="profile-photo"', 1)[1].split(">", 1)[0]
    assert 'loading="lazy"' not in portrait

    for project in FEATURED_PROJECTS:
        assert project.screenshot_master in content
        for path, width in project.webp_variants:
            assert f"{path} {width}w" in content
    assert content.count('loading="lazy"') == 4
    assert content.count('loading="eager"') == 1
    assert content.count('decoding="async"') == 5


def test_background_authority_and_reduced_motion_contract_are_preserved() -> None:
    home_css = HOME_CSS.read_text(encoding="utf-8")
    site_css = SITE_CSS.read_text(encoding="utf-8")

    assert 'url("../images/background/homepage-background-desktop-02.png")' in home_css
    assert 'url("../images/background/homepage-background-desktop.png")' not in home_css
    assert "@media (prefers-reduced-motion: reduce)" in site_css
    reduced = site_css.split("@media (prefers-reduced-motion: reduce)", 1)[1]
    assert "scroll-behavior: auto" in reduced
    assert "transform: none" in reduced
    assert "display: none" not in reduced


def test_all_fit_states_remain_candidates_without_block_12_promotion() -> None:
    home_css = HOME_CSS.read_text(encoding="utf-8")
    site_css = SITE_CSS.read_text(encoding="utf-8")
    responsive_css = home_css + site_css

    for fit_id in (
        "FIT-HDR-001",
        "FIT-HERO-001",
        "FIT-ENG-001",
        "FIT-ENG-002",
        "FIT-PRJ-001",
        "FIT-PRJ-002",
        "FIT-PRC-001",
        "FIT-PRC-002",
        "FIT-PRC-003",
        "FIT-EVD-001",
        "FIT-EVD-002",
        "FIT-EVD-003",
        "FIT-FTR-001",
    ):
        assert fit_id in responsive_css
    assert "FIT-TESTED" not in responsive_css
    assert "FIT-VALIDATED" not in responsive_css
