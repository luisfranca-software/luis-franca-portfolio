"""Approved professional skills dataset for the Skills module.

Governing documents: SPEC-001 (SPEC-001-REQ-005), ARCH-001 (14.2, 15.7).

The skills below are explicitly approved Product Owner content. They are not
inferred from project technologies or dependency files.

English remains the canonical source. Runtime translation is performed in the
presentation layer so the dataset itself stays stable and testable.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SkillGroup:
    """A named group of approved professional skills."""

    name: str
    skills: tuple[str, ...]


SKILL_GROUPS: tuple[SkillGroup, ...] = (
    SkillGroup(
        name="Software Engineering",
        skills=(
            "Software Architecture",
            "Requirements Engineering",
            "Specification-Driven Development",
            "Object-Oriented Programming",
            "REST API Design",
            "Software Documentation",
        ),
    ),
    SkillGroup(
        name="Backend & Python",
        skills=(
            "Python",
            "Django",
            "FastAPI",
            "Flask",
            "Pydantic",
            "SQLAlchemy",
        ),
    ),
    SkillGroup(
        name="Data & Integration",
        skills=(
            "PostgreSQL",
            "SQLite",
            "Relational Databases",
            "REST APIs",
            "External API Integration",
        ),
    ),
    SkillGroup(
        name="Testing & Quality",
        skills=(
            "pytest",
            "Automated Testing",
            "Unit Testing",
            "Integration Testing",
            "Acceptance Testing",
            "Ruff",
            "mypy",
        ),
    ),
    SkillGroup(
        name="AI & Automation",
        skills=(
            "LLM Integration",
            "AI-Assisted Software Engineering",
            "Prompt Engineering",
            "Workflow Automation",
            "RPA",
        ),
    ),
    SkillGroup(
        name="DevOps & Delivery",
        skills=(
            "Git",
            "GitHub",
            "Docker",
            "CI/CD",
            "GitHub Actions",
            "Linux",
        ),
    ),
    SkillGroup(
        name="Desktop Development",
        skills=("Tkinter",),
    ),
)
