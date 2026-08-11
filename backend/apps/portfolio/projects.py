"""Featured project dataset for the Portfolio module.

Governing documents: SPEC-003 (SPEC-003-REQ-001, REQ-002, REQ-003, REQ-004,
REQ-007, section 10), ARCH-001 (14.4, 15.7).

Release 1 presents three featured projects (SPEC-003-REQ-002) using the
approved Product Owner data. The dataset is code-defined but shaped to remain
compatible with future database-backed project persistence (SPEC-003-REQ-007):
every entry carries a unique identifier and a display order, and each
screenshot path maps to a tracked repository asset under
``frontend/static/images/projects/``.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    """Presentation data for a featured software project (SPEC-003 section 10)."""

    slug: str
    title: str
    summary: str
    technologies: tuple[str, ...]
    screenshot_master: str
    screenshot_width: int
    screenshot_height: int
    webp_variants: tuple[tuple[str, int], ...]
    github_url: str
    order: int
    governance_model: str
    demo_url: str | None = None


FEATURED_PROJECTS: tuple[Project, ...] = (
    Project(
        slug="enterprise-platform",
        title="Enterprise Platform",
        summary=(
            "Enterprise-grade web platform demonstrating specification-driven "
            "software engineering, modular architecture, security, automated "
            "testing, DevOps, observability, and software governance across "
            "the full development lifecycle."
        ),
        technologies=(
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
        screenshot_master="images/projects/enterprise-platform.png",
        screenshot_width=1480,
        screenshot_height=16384,
        webp_variants=(
            ("images/projects/enterprise-platform-900.webp", 900),
            ("images/projects/enterprise-platform-450.webp", 450),
        ),
        github_url="https://github.com/luisfranca-software/enterprise-platform",
        order=1,
        governance_model=(
            "Specification-Driven Development with human-governed architecture, "
            "implementation, technical review, and release approval."
        ),
    ),
    Project(
        slug="intelligent-currency-platform",
        title="Intelligent Currency Platform",
        summary=(
            "Modular currency intelligence platform for querying, tracking, "
            "forecasting, and analyzing exchange rates. Developed incrementally "
            "through successive releases, it combines API integration, "
            "PostgreSQL, automated testing, Docker, CI/CD, machine learning, "
            "and AI capabilities while maintaining software engineering and "
            "architectural discipline."
        ),
        technologies=(
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
        screenshot_master="images/projects/intelligent-currency-platform.png",
        screenshot_width=1480,
        screenshot_height=16384,
        webp_variants=(
            ("images/projects/intelligent-currency-platform-900.webp", 900),
            ("images/projects/intelligent-currency-platform-450.webp", 450),
        ),
        github_url=(
            "https://github.com/luisfranca-software/intelligent-currency-platform"
        ),
        order=2,
        governance_model=(
            "Specification-Driven Development with human-governed architecture, "
            "implementation, technical review, and release approval."
        ),
    ),
    Project(
        slug="currency-quotation-system",
        title="Currency Quotation System — Python RPA",
        summary=(
            "Python RPA application for automated currency quotation queries "
            "through an external API, featuring historical data, a graphical "
            "interface, and report generation. The project documents an "
            "architectural evolution from an initial object-oriented design to "
            "a complete MVC structure supported by automated tests and mocks."
        ),
        technologies=(
            "Python 3.12",
            "Requests",
            "Pandas",
            "Pytest",
            "OpenPyXL",
            "TkCalendar",
            "Mocks",
            "MVC",
        ),
        screenshot_master="images/projects/sistema_cotacao_moedas.png",
        screenshot_width=1480,
        screenshot_height=7636,
        webp_variants=(
            ("images/projects/sistema_cotacao_moedas-900.webp", 900),
            ("images/projects/sistema_cotacao_moedas-450.webp", 450),
        ),
        github_url="https://github.com/luisfranca-software/sistema_cotacao_moedas",
        order=3,
        governance_model=(
            "Specification-Driven Development with human-governed architecture, "
            "implementation, technical review, and release approval."
        ),
    ),
)
