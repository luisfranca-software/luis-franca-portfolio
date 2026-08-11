"""Unit tests for the Portfolio featured project dataset.

Governing documents: SPEC-003 (SPEC-003-REQ-002, REQ-004, REQ-007, section 10).

The dataset is validated against the approved Product Owner data: exact order,
titles, summaries, technology lists, governance models and GitHub URLs, with
no demonstration URLs in Release 1.
"""

from apps.portfolio.projects import FEATURED_PROJECTS

APPROVED_TITLES = (
    "Enterprise Platform",
    "Intelligent Currency Platform",
    "Currency Quotation System — Python RPA",
)

APPROVED_SUMMARIES = (
    "Enterprise-grade web platform demonstrating specification-driven "
    "software engineering, modular architecture, security, automated testing, "
    "DevOps, observability, and software governance across the full "
    "development lifecycle.",
    "Modular currency intelligence platform for querying, tracking, "
    "forecasting, and analyzing exchange rates. Developed incrementally "
    "through successive releases, it combines API integration, PostgreSQL, "
    "automated testing, Docker, CI/CD, machine learning, and AI capabilities "
    "while maintaining software engineering and architectural discipline.",
    "Python RPA application for automated currency quotation queries through "
    "an external API, featuring historical data, a graphical interface, and "
    "report generation. The project documents an architectural evolution from "
    "an initial object-oriented design to a complete MVC structure supported "
    "by automated tests and mocks.",
)

APPROVED_TECHNOLOGIES = (
    (
        "Python 3.12",
        "Django 6",
        "PostgreSQL 16",
        "Redis 7",
        "Nginx",
        "Docker",
        "Docker Compose",
        "GitHub Actions",
        "django-environ",
        "OpenCode",
    ),
    (
        "Python 3.12",
        "FastAPI",
        "PostgreSQL 16",
        "Pytest",
        "Docker",
        "Docker Compose",
        "GitHub Actions",
        "AI/ML",
        "OpenCode",
    ),
    (
        "Python 3.12",
        "Requests",
        "Pandas",
        "Pytest",
        "OpenPyXL",
        "TkCalendar",
        "Mocks",
        "MVC",
    ),
)

APPROVED_GITHUB_URLS = (
    "https://github.com/luisfranca-software/enterprise-platform",
    "https://github.com/luisfranca-software/intelligent-currency-platform",
    "https://github.com/luisfranca-software/sistema_cotacao_moedas",
)

APPROVED_GOVERNANCE_MODELS = (
    "Specification-Driven Development with human-governed architecture, "
    "implementation, technical review, and release approval.",
) * 3


def test_three_featured_projects_are_defined() -> None:
    assert len(FEATURED_PROJECTS) == 3


def test_slugs_are_unique() -> None:
    slugs = [project.slug for project in FEATURED_PROJECTS]
    assert len(slugs) == len(set(slugs))


def test_display_order_matches_approved_order() -> None:
    orders = [project.order for project in FEATURED_PROJECTS]
    assert orders == [1, 2, 3]


def test_titles_match_approved_data_in_order() -> None:
    assert tuple(project.title for project in FEATURED_PROJECTS) == APPROVED_TITLES


def test_summaries_match_approved_data_in_order() -> None:
    assert (
        tuple(project.summary for project in FEATURED_PROJECTS)
        == APPROVED_SUMMARIES
    )


def test_technologies_match_approved_data_in_order() -> None:
    assert (
        tuple(project.technologies for project in FEATURED_PROJECTS)
        == APPROVED_TECHNOLOGIES
    )


def test_github_urls_match_approved_owner_in_order() -> None:
    assert (
        tuple(project.github_url for project in FEATURED_PROJECTS)
        == APPROVED_GITHUB_URLS
    )


def test_no_forbidden_github_owner_is_used() -> None:
    for project in FEATURED_PROJECTS:
        assert "github.com/luis-franca/" not in project.github_url


def test_governance_models_match_approved_data() -> None:
    assert (
        tuple(project.governance_model for project in FEATURED_PROJECTS)
        == APPROVED_GOVERNANCE_MODELS
    )


def test_all_demo_urls_are_none() -> None:
    for project in FEATURED_PROJECTS:
        assert project.demo_url is None


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
