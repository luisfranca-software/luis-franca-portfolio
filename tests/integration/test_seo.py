"""Integration tests for the SEO foundation (SPEC-001 section 10)."""

from django.test import Client


def test_home_page_has_meta_description() -> None:
    content = Client().get("/").content.decode()

    assert '<meta name="description"' in content
    assert "Software Engineer specializing in Python backend" in content


def test_home_page_has_canonical_url() -> None:
    content = Client().get("/").content.decode()

    assert '<link rel="canonical"' in content


def test_home_page_has_open_graph_tags() -> None:
    content = Client().get("/").content.decode()

    assert 'property="og:title"' in content
    assert 'property="og:description"' in content
    assert 'property="og:type"' in content
    assert 'property="og:url"' in content
    assert "Luís França — Software Engineer" in content


def test_favicon_links_present() -> None:
    content = Client().get("/").content.decode()

    assert 'rel="icon"' in content
    assert 'rel="apple-touch-icon"' in content
    assert "favicon-32x32.png" in content
    assert "apple-touch-icon.png" in content
