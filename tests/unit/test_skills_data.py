"""Unit tests for the approved professional skills dataset.

Governing documents: SPEC-001 (SPEC-001-REQ-005).
"""

from apps.skills.skills import SKILL_GROUPS

APPROVED_GROUPS = (
    "Software Engineering",
    "Backend & Python",
    "Data & Integration",
    "Testing & Quality",
    "AI & Automation",
    "DevOps & Delivery",
    "Desktop Development",
)

APPROVED_SKILLS = (
    "Software Architecture",
    "Requirements Engineering",
    "Specification-Driven Development",
    "Object-Oriented Programming",
    "REST API Design",
    "Software Documentation",
    "Python",
    "Django",
    "FastAPI",
    "Flask",
    "Pydantic",
    "SQLAlchemy",
    "PostgreSQL",
    "SQLite",
    "Relational Databases",
    "REST APIs",
    "External API Integration",
    "pytest",
    "Automated Testing",
    "Unit Testing",
    "Integration Testing",
    "Acceptance Testing",
    "Ruff",
    "mypy",
    "LLM Integration",
    "AI-Assisted Software Engineering",
    "Prompt Engineering",
    "Workflow Automation",
    "RPA",
    "Git",
    "GitHub",
    "Docker",
    "CI/CD",
    "GitHub Actions",
    "Linux",
    "Tkinter",
)


def test_skill_groups_match_approved_names() -> None:
    assert tuple(group.name for group in SKILL_GROUPS) == APPROVED_GROUPS


def test_all_approved_skills_are_present() -> None:
    all_skills = [skill for group in SKILL_GROUPS for skill in group.skills]

    for skill in APPROVED_SKILLS:
        assert skill in all_skills


def test_no_unapproved_skills_are_present() -> None:
    all_skills = [skill for group in SKILL_GROUPS for skill in group.skills]

    for skill in all_skills:
        assert skill in APPROVED_SKILLS


def test_skill_groups_are_non_empty() -> None:
    for group in SKILL_GROUPS:
        assert group.name
        assert group.skills
