"""Integration tests for the footer (SPEC-001-REQ-009)."""

import pytest
from django.test import Client

PAGE_PATHS = ("/", "/about/", "/skills/", "/experience/", "/portfolio/", "/contact/")


@pytest.mark.parametrize("path", PAGE_PATHS)
def test_footer_appears_on_every_page(path: str) -> None:
    content = Client().get(path).content.decode()

    assert '<footer class="site-footer' in content
    assert "© " in content
    assert "Luís França" in content


@pytest.mark.parametrize("path", PAGE_PATHS[1:])
def test_footer_contains_navigation_shortcuts(path: str) -> None:
    content = Client().get(path).content.decode()

    if path == "/contact/":
        assert 'aria-label="Footer navigation"' in content
        assert 'href="/#projects"' in content
        assert 'href="/contact/"' in content
        assert 'aria-current="page"' in content
        assert 'class="homepage-footer__tagline"' in content
        assert "Engineering with evidence." in content
        return
    assert "Navigation" in content
    assert 'href="/"' in content
    assert 'href="/about/"' in content
    assert 'href="/skills/"' in content
    assert 'href="/experience/"' in content
    assert 'href="/portfolio/"' in content
    assert 'href="/contact/"' in content


def test_footer_contains_professional_links(contact_links) -> None:
    content = Client().get("/about/").content.decode()

    assert "Professional links" in content
    assert contact_links["linkedin"] in content
    assert contact_links["github"] in content
    assert contact_links["resume"] in content


def test_footer_does_not_duplicate_whatsapp_link(contact_links) -> None:
    content = Client().get("/").content.decode()

    # Header WhatsApp is the canonical persistent entry point and must not be
    # duplicated in the Footer professional links.
    footer_section = content.split("Professional links")[1]
    footer_professional_links = footer_section.split("</footer>")[0]
    assert contact_links["whatsapp"] not in footer_professional_links


def test_homepage_footer_contact_link_is_not_marked_as_current() -> None:
    content = Client().get("/").content.decode()
    footer = content.split('<footer class="site-footer', maxsplit=1)[1]

    assert 'href="#contact"' in footer
    assert 'href="#contact" aria-current="page"' not in footer
