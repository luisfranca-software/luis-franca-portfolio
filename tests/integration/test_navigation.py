"""Integration tests for global navigation (SPEC-001-REQ-002, SPEC-001-REQ-008)."""

import pytest
from django.test import Client

PAGE_PATHS = ("/", "/about/", "/skills/", "/experience/", "/portfolio/", "/contact/")


def _navigation(content: str) -> str:
    return content.split('<nav class="site-nav"', maxsplit=1)[1].split(
        "</nav>", maxsplit=1
    )[0]


@pytest.mark.parametrize("path", PAGE_PATHS[1:])
def test_existing_route_navigation_appears_on_non_homepage_routes(path: str) -> None:
    navigation = _navigation(Client().get(path).content.decode())

    assert 'href="/"' in navigation
    if path == "/contact/":
        assert "data-contact-navigation" in navigation
        assert 'href="/#engineering"' in navigation
        assert 'href="/#projects"' in navigation
        for legacy_path in ("/about/", "/skills/", "/experience/", "/portfolio/"):
            assert f'href="{legacy_path}"' not in navigation
        return
    assert 'href="/about/"' in navigation
    assert 'href="/skills/"' in navigation
    assert 'href="/experience/"' in navigation
    assert 'href="/portfolio/"' in navigation
    assert 'href="/contact/"' in navigation


def test_homepage_navigation_uses_approved_fragment_destinations() -> None:
    navigation = _navigation(Client().get("/").content.decode())

    for label, fragment in (
        ("Engineering", "#engineering"),
        ("Projects", "#projects"),
        ("Process", "#process"),
        ("Contact", "#contact"),
    ):
        assert f'href="{fragment}"' in navigation
        assert f">{label}</a>" in navigation

    assert 'href="/about/"' not in navigation
    assert 'href="/skills/"' not in navigation
    assert 'href="/experience/"' not in navigation
    assert 'href="/portfolio/"' not in navigation


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_skip_link_appears_on_every_page(path: str) -> None:
    content = Client().get(path).content.decode()

    assert 'class="skip-link"' in content
    assert 'href="#main-content"' in content


def test_navigation_toggle_is_keyboard_accessible() -> None:
    content = Client().get("/").content.decode()

    assert 'class="site-nav__toggle"' in content
    assert 'aria-expanded="false"' in content
    assert 'aria-controls="site-nav-menu"' in content


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_configured_whatsapp_is_one_secure_header_action(
    path: str, contact_links
) -> None:
    content = Client().get(path).content.decode()
    navigation = _navigation(content)

    assert content.count("site-nav__whatsapp") == 1
    assert contact_links["whatsapp"] in navigation
    assert 'target="_blank"' in navigation
    assert 'rel="noopener noreferrer"' in navigation
    assert 'aria-label="Chat on WhatsApp"' in navigation
    assert "whatsapp-button" not in content


def test_unconfigured_whatsapp_renders_no_header_action(settings) -> None:
    settings.CONTACT_LINKS = {**settings.CONTACT_LINKS, "whatsapp": ""}
    content = Client().get("/").content.decode()

    assert "site-nav__whatsapp" not in content
    assert "whatsapp-button" not in content


@pytest.mark.parametrize("path", PAGE_PATHS[1:])
def test_homepage_responsive_scope_is_not_loaded_on_unrelated_routes(path: str) -> None:
    content = Client().get(path).content.decode()

    assert "site-main--homepage" not in content
    assert 'class="homepage"' not in content
    assert 'href="/static/css/home.css"' not in content
