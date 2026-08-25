"""Integration tests for the Home page (SPEC-001-REQ-003)."""

import re
from urllib.parse import urlparse

from django.test import Client


def test_home_page_renders() -> None:
    response = Client().get("/")

    assert response.status_code == 200


def test_home_page_presents_approved_identity() -> None:
    content = Client().get("/").content.decode()

    assert "Luís França" in content
    assert "Luís Eduardo Carvalho França" in content


def test_home_page_presents_all_approved_titles() -> None:
    content = Client().get("/").content.decode()

    assert "Software Engineer" in content
    assert "Python Backend Engineer" in content
    assert "AI/LLM Engineer" in content


def test_home_page_presents_primary_cta() -> None:
    content = Client().get("/").content.decode()

    # The apostrophe is HTML-escaped by Django's default autoescaping.
    assert "Let&#x27;s Talk" in content
    assert 'href="/contact/"' in content


def test_home_page_includes_profile_photo() -> None:
    content = Client().get("/").content.decode()

    assert "images/profile/luis-franca-transparent-02.png" in content
    assert "Professional photograph of Luís Eduardo Carvalho França" in content


def test_home_page_preserves_identity_and_photo() -> None:
    content = Client().get("/").content.decode()

    assert "Luís França" in content
    assert "Luís Eduardo Carvalho França" in content
    assert "Software Engineer" in content
    assert "images/profile/luis-franca-transparent-02.png" in content


def test_home_page_loads_scoped_responsive_foundations() -> None:
    content = Client().get("/").content.decode()

    assert 'class="site-main site-main--homepage"' in content
    assert 'class="homepage"' in content
    assert 'class="home-hero homepage__container homepage__section"' in content
    stylesheet = re.search(r'href="([^"]*?/static/css/home\.css(?:\?[^"]*)?)"', content)

    assert stylesheet is not None
    assert urlparse(stylesheet.group(1)).path == "/static/css/home.css"
