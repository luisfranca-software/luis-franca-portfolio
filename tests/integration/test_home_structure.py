"""Semantic Homepage structure tests for SDD-RWD-001 Block 2."""

from django.test import Client

from apps.portfolio.projects import FEATURED_PROJECTS


def _home_content() -> str:
    return Client().get("/").content.decode()


def test_homepage_sections_follow_approved_semantic_order() -> None:
    content = _home_content()
    section_markers = (
        'id="home"',
        'id="engineering"',
        'id="projects"',
        'id="process"',
        'id="evidence"',
        'id="contact"',
    )

    positions = [content.index(marker) for marker in section_markers]
    assert positions == sorted(positions)
    assert all(content.count(marker) == 1 for marker in section_markers)


def test_homepage_has_one_h1_and_major_section_h2_headings() -> None:
    content = _home_content()

    assert content.count("<h1") == 1
    for heading_id in (
        "engineering-heading",
        "projects-heading",
        "process-heading",
        "evidence-heading",
        "contact-heading",
    ):
        assert f'id="{heading_id}"' in content


def test_homepage_renders_four_ordered_engineering_capabilities() -> None:
    content = _home_content()
    slugs = (
        "backend-engineering",
        "software-architecture",
        "apis-automation",
        "ai-intelligent-systems",
    )

    markers = [f'data-engineering-item="{slug}"' for slug in slugs]
    assert [content.index(marker) for marker in markers] == sorted(
        content.index(marker) for marker in markers
    )
    assert content.count("data-engineering-item=") == 4


def test_homepage_reuses_featured_projects_in_canonical_order() -> None:
    response = Client().get("/")
    content = response.content.decode()

    assert response.context["featured_projects"] is FEATURED_PROJECTS
    markers = [f'data-home-project="{project.slug}"' for project in FEATURED_PROJECTS]
    assert [content.index(marker) for marker in markers] == sorted(
        content.index(marker) for marker in markers
    )
    assert content.count("data-home-project=") == len(FEATURED_PROJECTS)


def test_homepage_renders_one_ordered_seven_step_process() -> None:
    content = _home_content()
    slugs = (
        "requirements",
        "specification",
        "architecture",
        "implementation",
        "testing",
        "deployment",
        "validation",
    )

    markers = [f'data-process-step="{slug}"' for slug in slugs]
    assert [content.index(marker) for marker in markers] == sorted(
        content.index(marker) for marker in markers
    )
    assert content.count("data-process-step=") == 7


def test_homepage_renders_four_approved_evidence_themes() -> None:
    content = _home_content()
    slugs = ("architecture", "quality-first", "delivery", "governance")

    markers = [f'data-evidence-theme="{slug}"' for slug in slugs]
    assert [content.index(marker) for marker in markers] == sorted(
        content.index(marker) for marker in markers
    )
    assert content.count("data-evidence-theme=") == 4


def test_contact_cta_uses_existing_contact_route() -> None:
    content = _home_content()
    contact_section = content[content.index('id="contact"') :]

    assert 'href="/contact/"' in contact_section


def test_homepage_preserves_route_aware_navigation_and_reserved_visual() -> None:
    content = _home_content()

    assert content.count('class="home-ai-rag" aria-hidden="true"') == 1
    assert content.count("site-nav__whatsapp") == 1
    assert "whatsapp-button" not in content
    assert 'href="#engineering"' in content
    assert 'href="#projects"' in content
    assert 'href="#process"' in content
    assert 'href="#contact"' in content
