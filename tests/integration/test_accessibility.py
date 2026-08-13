"""Integration tests for accessibility baseline (SPEC-001 section 9)."""

import pytest
from django.test import Client

PAGE_PATHS = ("/", "/about/", "/skills/", "/experience/", "/portfolio/", "/contact/")


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_pages_have_main_landmark(path: str) -> None:
    content = Client().get(path).content.decode()

    assert '<main id="main-content"' in content


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_pages_have_header_and_footer_landmarks(path: str) -> None:
    content = Client().get(path).content.decode()

    assert "<header" in content
    assert "<footer" in content


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_navigation_uses_semantic_list(path: str) -> None:
    content = Client().get(path).content.decode()

    assert '<nav class="site-nav"' in content
    assert '<ul class="site-nav__menu"' in content


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_navigation_does_not_use_application_menu_roles(path: str) -> None:
    content = Client().get(path).content.decode()

    assert 'role="menubar"' not in content
    assert 'role="menuitem"' not in content
    assert 'role="none"' not in content


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_images_have_descriptive_alt_text(path: str) -> None:
    content = Client().get(path).content.decode()

    # Only pages that include images require alt text verification.
    if "<img" not in content:
        return

    assert 'alt="' in content
    assert 'alt=""' not in content


def test_home_page_has_single_h1() -> None:
    content = Client().get("/").content.decode()

    assert content.count("<h1") == 1
    assert "Luís França" in content
