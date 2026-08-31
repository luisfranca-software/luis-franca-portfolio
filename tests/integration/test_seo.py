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


def test_robots_txt_allows_all_crawlers_and_points_to_sitemap() -> None:
    response = Client().get("/robots.txt")

    assert response.status_code == 200
    content = response.content.decode()
    assert "User-agent: *" in content
    assert "Allow: /" in content
    assert "/sitemap.xml" in content


def test_home_page_has_og_image() -> None:
    content = Client().get("/").content.decode()

    assert 'property="og:image"' in content
    assert "luis-franca-transparent-02.png" in content
    assert 'property="og:image:width"' in content
    assert 'property="og:image:height"' in content


def test_home_page_has_twitter_card() -> None:
    content = Client().get("/").content.decode()

    assert 'name="twitter:card"' in content
    assert 'name="twitter:title"' in content
    assert 'name="twitter:image"' in content
