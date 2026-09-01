"""Unit tests for the IA Jujuju prompt builder.

Governing documents: SPEC-005 §20–21, §56.
"""

from __future__ import annotations

import pytest

from apps.assistant.services.prompt_builder import PromptBuilder


@pytest.fixture
def builder() -> PromptBuilder:
    return PromptBuilder()


def test_system_prompt_establishes_identity(builder: PromptBuilder) -> None:
    prompt = builder.build_system_prompt("en")

    assert "IA Jujuju" in prompt
    assert "Luís França" in prompt


def test_system_prompt_english(builder: PromptBuilder) -> None:
    prompt = builder.build_system_prompt("en")

    assert "Knowledge Base context" in prompt
    assert "English" in prompt


def test_system_prompt_portuguese(builder: PromptBuilder) -> None:
    prompt = builder.build_system_prompt("pt-br")

    assert "Base de Conhecimento" in prompt
    assert "português" in prompt.lower()


def test_system_prompt_forbids_unsupported_claims(builder: PromptBuilder) -> None:
    prompt = builder.build_system_prompt("en")

    assert "internet" in prompt.lower()
    assert "administrative" in prompt.lower() or "administrativ" in prompt.lower()
    assert "reveal" in prompt.lower() or "credentials" in prompt.lower()


def test_user_prompt_includes_actual_question(builder: PromptBuilder) -> None:
    prompt = builder.build_user_prompt(
        "en",
        "What is Python?",
    )

    assert "What is Python?" in prompt
    assert "Visitor question:" in prompt


def test_user_prompt_does_not_embed_context(builder: PromptBuilder) -> None:
    prompt = builder.build_user_prompt(
        "en",
        "What is Python?",
    )

    assert "[Source 1]" not in prompt
    assert "Python is a language" not in prompt


def test_user_prompt_missing_knowledge(builder: PromptBuilder) -> None:
    prompt = builder.build_user_prompt(
        "en",
        "What is Python?",
        has_evidence=False,
    )

    assert "does not contain sufficient information" in prompt
    assert "What is Python?" in prompt


def test_user_prompt_missing_knowledge_portuguese(builder: PromptBuilder) -> None:
    prompt = builder.build_user_prompt(
        "pt-br",
        "O que é Python?",
        has_evidence=False,
    )

    assert "não contém informações suficientes" in prompt
    assert "O que é Python?" in prompt


def test_system_prompt_is_server_controlled(builder: PromptBuilder) -> None:
    prompt = builder.build_system_prompt("en")

    assert "You are IA Jujuju" in prompt
    assert "rules" in prompt.lower()
