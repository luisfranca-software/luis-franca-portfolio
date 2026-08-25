"""Ordered presentation content for the Release 1.1 Homepage.

This module owns immutable Homepage-only presentation data. Canonical project
identity remains owned by ``apps.portfolio.projects`` and is not duplicated
here (SDD-RWD-001, RWD-FR-002 and RWD-FR-011 through RWD-FR-017).
"""

from dataclasses import dataclass

from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _


@dataclass(frozen=True)
class EngineeringCapability:
    """One approved Engineering capability in semantic display order."""

    slug: str
    ordinal: str
    title: Promise
    description: Promise


@dataclass(frozen=True)
class ProcessStep:
    """One step in the single approved seven-step engineering process."""

    slug: str
    ordinal: str
    title: Promise
    description: Promise


@dataclass(frozen=True)
class EvidenceTheme:
    """One approved Professional Evidence theme."""

    slug: str
    title: Promise
    description: Promise


ENGINEERING_CAPABILITIES: tuple[EngineeringCapability, ...] = (
    EngineeringCapability(
        slug="backend-engineering",
        ordinal="01",
        title=_("Backend Engineering"),
        description=_(
            "Robust Python services, domain logic, persistence, and "
            "production-ready backend systems."
        ),
    ),
    EngineeringCapability(
        slug="software-architecture",
        ordinal="02",
        title=_("Software Architecture"),
        description=_(
            "Modular boundaries, explicit interfaces, specification-driven "
            "decisions, and maintainable delivery."
        ),
    ),
    EngineeringCapability(
        slug="apis-automation",
        ordinal="03",
        title=_("APIs & Automation"),
        description=_(
            "API integrations, workflow automation, testing, and reliable "
            "connections between systems."
        ),
    ),
    EngineeringCapability(
        slug="ai-intelligent-systems",
        ordinal="04",
        title=_("AI & Intelligent Systems"),
        description=_(
            "AI/LLM capabilities developed with engineering discipline, "
            "traceability, and product purpose."
        ),
    ),
)


PROCESS_STEPS: tuple[ProcessStep, ...] = (
    ProcessStep(
        "requirements",
        "01",
        _("Requirements"),
        _("Clarify goals, constraints, users, and measurable outcomes."),
    ),
    ProcessStep(
        "specification",
        "02",
        _("Specification"),
        _("Translate requirements into explicit behavior and acceptance criteria."),
    ),
    ProcessStep(
        "architecture",
        "03",
        _("Architecture"),
        _("Shape boundaries, interfaces, data flow, and technical trade-offs."),
    ),
    ProcessStep(
        "implementation",
        "04",
        _("Implementation"),
        _("Build maintainable software from the approved technical direction."),
    ),
    ProcessStep(
        "testing",
        "05",
        _("Testing"),
        _("Verify behavior, resilience, accessibility, and regression safety."),
    ),
    ProcessStep(
        "deployment",
        "06",
        _("Deployment"),
        _("Release through controlled automation and observable environments."),
    ),
    ProcessStep(
        "validation",
        "07",
        _("Validation"),
        _("Measure outcomes and feed evidence into the next iteration."),
    ),
)


EVIDENCE_THEMES: tuple[EvidenceTheme, ...] = (
    EvidenceTheme(
        "architecture",
        _("Architecture"),
        _("Explicit boundaries, modular design, and documented technical decisions."),
    ),
    EvidenceTheme(
        "quality-first",
        _("Quality First"),
        _("Automated testing and regression safety across project delivery."),
    ),
    EvidenceTheme(
        "delivery",
        _("Delivery"),
        _("Containerized environments, CI/CD, observability, and controlled releases."),
    ),
    EvidenceTheme(
        "governance",
        _("Governance"),
        _("Specification-driven work with human review and release approval."),
    ),
)
