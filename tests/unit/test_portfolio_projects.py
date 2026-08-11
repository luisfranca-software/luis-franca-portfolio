"""Unit tests for the Portfolio featured project dataset.

Governing documents: SPEC-003 (SPEC-003-REQ-002, REQ-004, REQ-007, section 10).
"""

from apps.portfolio.projects import FEATURED_PROJECTS


def test_three_featured_projects_are_defined() -> None:
    assert len(FEATURED_PROJECTS) == 3


def test_slugs_are_unique() -> None:
    slugs = [project.slug for project in FEATURED_PROJECTS]
    assert len(slugs) == len(set(slugs))


def test_display_order_is_unique_and_increasing() -> None:
    orders = [project.order for project in FEATURED_PROJECTS]
    assert orders == sorted(orders)
    assert len(orders) == len(set(orders))


def test_each_project_defines_required_data() -> None:
    for project in FEATURED_PROJECTS:
        assert project.title
        assert project.summary
        assert project.technologies
        assert project.screenshot_master
        assert project.screenshot_width > 0
        assert project.screenshot_height > 0
        assert project.webp_variants
        assert project.github_url


def test_each_project_maps_a_screenshot_master_and_variants() -> None:
    for project in FEATURED_PROJECTS:
        assert project.screenshot_master.startswith("images/projects/")
        for path, width in project.webp_variants:
            assert path.startswith("images/projects/")
            assert width > 0


def test_demo_link_is_optional() -> None:
    assert any(project.demo_url for project in FEATURED_PROJECTS)
    assert any(project.demo_url is None for project in FEATURED_PROJECTS)
