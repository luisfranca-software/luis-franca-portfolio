"""Focused tests for the discreet administrative access link in the shared footer."""

import re

import pytest
from django.test import Client

ADMIN_FOOTER_PAGES = ("/", "/contact/", "/portfolio/")


def _footer(path: str = "/", language: str = "en") -> str:
    content = Client(HTTP_ACCEPT_LANGUAGE=language).get(path).content.decode()
    start = content.index('<footer class="site-footer')
    return content[start : content.index("</footer>", start)]


@pytest.mark.parametrize("path", ADMIN_FOOTER_PAGES)
def test_footer_renders_admin_link(path: str) -> None:
    footer = _footer(path)

    assert " · <a" in footer
    assert '<a href="/admin/">Admin</a>' in footer


@pytest.mark.parametrize("path", ADMIN_FOOTER_PAGES)
def test_admin_link_resolves_to_admin_root(path: str) -> None:
    footer = _footer(path)
    matches = re.findall(r'<a[^>]*href="(/admin/)"[^>]*>Admin</a>', footer)

    assert matches, f"Admin link not found or does not resolve to /admin/ on {path}"


def test_admin_link_is_a_real_anchor() -> None:
    footer = _footer("/")
    admin_link = re.search(r'<a[^>]*href="/admin/"[^>]*>Admin</a>', footer)

    assert admin_link is not None


@pytest.mark.parametrize("path", ADMIN_FOOTER_PAGES)
def test_copyright_text_is_preserved(path: str) -> None:
    footer = _footer(path)

    assert re.search(r"© \d{4} Luís França", footer)


@pytest.mark.parametrize("path", ADMIN_FOOTER_PAGES)
def test_admin_link_renders_in_portuguese(path: str) -> None:
    footer = _footer(path, language="pt-br")

    assert " · <a" in footer
    assert '<a href="/admin/">Admin</a>' in footer
