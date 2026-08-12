"""Integration tests for global navigation (SPEC-001-REQ-002, SPEC-001-REQ-008)."""

import pytest
from django.test import Client

PAGE_PATHS = ("/", "/about/", "/skills/", "/experience/", "/portfolio/", "/contact/")


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_global_navigation_appears_on_every_page(path: str) -> None:
    content = Client().get(path).content.decode()

    assert '<nav class="site-nav"' in content
    assert 'href="/"' in content
    assert 'href="/about/"' in content
    assert 'href="/skills/"' in content
    assert 'href="/experience/"' in content
    assert 'href="/portfolio/"' in content
    assert 'href="/contact/"' in content


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
