"""Integration tests for the Release 1 sitemap (PB-001 14.1, SPEC-001 section 10)."""

from django.test import Client

EXPECTED_PATHS = {
    "<loc>http://testserver/</loc>",
    "<loc>http://testserver/about/</loc>",
    "<loc>http://testserver/skills/</loc>",
    "<loc>http://testserver/experience/</loc>",
    "<loc>http://testserver/portfolio/</loc>",
    "<loc>http://testserver/contact/</loc>",
}


def test_sitemap_endpoint_renders() -> None:
    response = Client().get("/sitemap.xml")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/xml")


def test_sitemap_includes_public_release_1_pages() -> None:
    content = Client().get("/sitemap.xml").content.decode()

    for path in EXPECTED_PATHS:
        assert path in content


def test_sitemap_uses_absolute_urls() -> None:
    content = Client().get("/sitemap.xml").content.decode()

    assert "<loc>" in content
    assert "http://testserver" in content
