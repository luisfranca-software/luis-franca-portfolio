"""Unit tests for immutable ordered Homepage presentation content."""

from dataclasses import FrozenInstanceError

import pytest
from django.utils.translation import override

from apps.home.content import ENGINEERING_CAPABILITIES, EVIDENCE_THEMES, PROCESS_STEPS


def test_engineering_capabilities_are_approved_and_ordered() -> None:
    assert tuple(item.ordinal for item in ENGINEERING_CAPABILITIES) == (
        "01",
        "02",
        "03",
        "04",
    )
    with override("en"):
        assert tuple(str(item.title) for item in ENGINEERING_CAPABILITIES) == (
            "Backend Engineering",
            "Software Architecture",
            "APIs & Automation",
            "AI & Intelligent Systems",
        )


def test_process_uses_one_approved_seven_step_sequence() -> None:
    with override("en"):
        assert tuple(str(step.title) for step in PROCESS_STEPS) == (
            "Requirements",
            "Specification",
            "Architecture",
            "Implementation",
            "Testing",
            "Deployment",
            "Validation",
        )


def test_evidence_themes_are_approved_and_ordered() -> None:
    with override("en"):
        assert tuple(str(theme.title) for theme in EVIDENCE_THEMES) == (
            "Architecture",
            "Quality First",
            "Delivery",
            "Governance",
        )


def test_homepage_content_items_are_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        ENGINEERING_CAPABILITIES[0].slug = "changed"  # type: ignore[misc]
