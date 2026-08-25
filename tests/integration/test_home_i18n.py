"""Integration tests for Home page bilingual behavior (SPEC-001 section 8)."""

from django.test import Client


def test_home_page_renders_in_english_by_default() -> None:
    content = Client().get("/").content.decode()

    assert "Hello, I'm" in content
    assert "Software Engineer" in content
    assert "Python Backend Engineer" in content
    assert "AI/LLM Engineer" in content
    assert "Let&#x27;s Talk" in content
    assert "Vamos conversar" not in content


def test_home_page_renders_titles_in_portuguese() -> None:
    client = Client(HTTP_ACCEPT_LANGUAGE="pt-br")
    content = client.get("/").content.decode()

    assert "Olá, eu sou" in content
    assert "Vamos conversar" in content
    assert "Engenheiro de Software" in content
    assert "Engenheiro Python Backend" in content
    assert "Engenheiro de IA/LLM" in content
    # The approved English titles must not remain untranslated.
    assert "Software Engineer" not in content
    assert "Python Backend Engineer" not in content
    assert "AI/LLM Engineer" not in content


def test_home_page_renders_positioning_in_portuguese() -> None:
    client = Client(HTTP_ACCEPT_LANGUAGE="pt-br")
    content = client.get("/").content.decode()

    assert "engenharia de software focada em python" in content.lower()
    # The approved English positioning must not remain untranslated.
    assert "Software engineering focused on Python" not in content


def test_homepage_semantic_sections_render_in_portuguese() -> None:
    content = Client(HTTP_ACCEPT_LANGUAGE="pt-br").get("/").content.decode()

    assert "O que eu desenvolvo" in content
    assert "Engenharia Backend" in content
    assert "Trabalhos de Engenharia Selecionados" in content
    assert "Como eu trabalho" in content
    assert "Requisitos" in content
    assert "Evidências Profissionais" in content
    assert "Qualidade em Primeiro Lugar" in content
    assert "Vamos construir algo significativo" in content
    assert "Entre em contato" in content


def test_homepage_header_destinations_render_in_portuguese() -> None:
    content = Client(HTTP_ACCEPT_LANGUAGE="pt-br").get("/").content.decode()
    navigation = content.split('<nav class="site-nav"', maxsplit=1)[1].split(
        "</nav>", maxsplit=1
    )[0]

    assert ">Engenharia</a>" in navigation
    assert ">Projetos</a>" in navigation
    assert ">Processo</a>" in navigation
    assert ">Contato</a>" in navigation
