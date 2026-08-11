"""Featured project dataset for the Portfolio module.

Governing documents: SPEC-003 (SPEC-003-REQ-001, REQ-002, REQ-003, REQ-004,
REQ-007, section 10), ARCH-001 (14.4, 15.7).

Release 1 presents three featured projects (SPEC-003-REQ-002). The dataset is
code-defined but shaped to remain compatible with future database-backed
project persistence (SPEC-003-REQ-007): every entry carries a unique
identifier and a display order, and each screenshot path maps to a tracked
repository asset under ``frontend/static/images/projects/``.
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
    demo_url: str | None = None


FEATURED_PROJECTS: tuple[Project, ...] = (
    Project(
        slug="enterprise-platform",
        title="Enterprise Platform",
        summary=(
            "A modular enterprise management platform covering operations, "
            "inventory and reporting, with role-based access and multi-company "
            "support."
        ),
        technologies=("Python", "Django", "PostgreSQL", "JavaScript"),
        screenshot_master="images/projects/enterprise-platform.png",
        screenshot_width=1480,
        screenshot_height=16384,
        webp_variants=(
            ("images/projects/enterprise-platform-900.webp", 900),
            ("images/projects/enterprise-platform-450.webp", 450),
        ),
        github_url="https://github.com/luis-franca/enterprise-platform",
        demo_url="https://enterprise-platform.example.com",
        order=1,
    ),
    Project(
        slug="intelligent-currency-platform",
        title="Intelligent Currency Platform",
        summary=(
            "A currency intelligence platform that aggregates exchange rates "
            "and delivers analytical insights to support financial "
            "decision-making."
        ),
        technologies=("Python", "Django", "PostgreSQL", "Django REST Framework"),
        screenshot_master="images/projects/intelligent-currency-platform.png",
        screenshot_width=1480,
        screenshot_height=16384,
        webp_variants=(
            ("images/projects/intelligent-currency-platform-900.webp", 900),
            ("images/projects/intelligent-currency-platform-450.webp", 450),
        ),
        github_url="https://github.com/luis-franca/intelligent-currency-platform",
        demo_url="https://intelligent-currency-platform.example.com",
        order=2,
    ),
    Project(
        slug="currency-quotation-system",
        title="Currency Quotation System",
        summary=(
            "A system that tracks and compares currency quotations with "
            "automated rate updates and historical visualization."
        ),
        technologies=("Python", "Django", "PostgreSQL", "Bootstrap"),
        screenshot_master="images/projects/sistema_cotacao_moedas.png",
        screenshot_width=1480,
        screenshot_height=7636,
        webp_variants=(
            ("images/projects/sistema_cotacao_moedas-900.webp", 900),
            ("images/projects/sistema_cotacao_moedas-450.webp", 450),
        ),
        github_url="https://github.com/luis-franca/sistema-cotacao-moedas",
        order=3,
    ),
)
