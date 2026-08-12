"""Integration tests for the footer (SPEC-001-REQ-009)."""

import pytest
from django.test import Client

PAGE_PATHS = ("/", "/about/", "/skills/", "/experience/", "/portfolio/", "/contact/")


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_footer_appears_on_every_page(path: str) -> None:
    content = Client().get(path).content.decode()

    assert '<footer class="site-footer"' in content
    assert "All rights reserved" in content


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_footer_contains_navigation_shortcuts(path: str) -> None:
    content = Client().get(path).content.decode()

    assert "Navigation" in content
    assert 'href="/"' in content
    assert 'href="/about/"' in content
    assert 'href="/skills/"' in content
    assert 'href="/experience/"' in content
    assert 'href="/portfolio/"' in content
    assert 'href="/contact/"' in content


def test_footer_contains_professional_links(contact_links) -> None:
    content = Client().get("/").content.decode()

    assert "Professional links" in content
    assert contact_links["linkedin"] in content
    assert contact_links["github"] in content
    assert contact_links["whatsapp"] in content
    assert contact_links["resume"] in content
