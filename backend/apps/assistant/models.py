"""IA Jujuju conversation persistence models.

Governing documents: ADR-007, SPEC-005.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class ConversationLanguage(models.TextChoices):
    """Supported assistant interaction languages (SPEC-005 §6)."""

    EN = "en", _("English")
    PT_BR = "pt-br", _("Portuguese (Brazil)")


class ConversationStatus(models.TextChoices):
    """Controlled conversation lifecycle statuses (SPEC-005 §10)."""

    ACTIVE = "active", _("Active")
    FAILED = "failed", _("Failed")


class MessageRole(models.TextChoices):
    """Persisted conversation message roles (SPEC-005 §12)."""

    USER = "user", _("User")
    ASSISTANT = "assistant", _("Assistant")


class Conversation(models.Model):
    """Anonymous session-bound assistant interaction thread (SPEC-005 §9)."""

    session_key = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_("session key"),
        help_text=_("Anonymous session association for continuity; not verified identity."),
    )
    language = models.CharField(
        max_length=10,
        choices=ConversationLanguage.choices,
        verbose_name=_("language"),
    )
    status = models.CharField(
        max_length=16,
        choices=ConversationStatus.choices,
        default=ConversationStatus.ACTIVE,
        verbose_name=_("status"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = _("conversation")
        verbose_name_plural = _("conversations")

    def __str__(self) -> str:
        return f"{self.pk} ({self.language})"

    def clean(self) -> None:
        super().clean()
        if not self.session_key or not self.session_key.strip():
            raise ValidationError({"session_key": _("Session association is required.")})


class ConversationMessage(models.Model):
    """Ordered message within a conversation (SPEC-005 §11)."""

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("conversation"),
    )
    sequence = models.PositiveIntegerField(
        verbose_name=_("sequence"),
        help_text=_("Deterministic order within the conversation."),
    )
    role = models.CharField(
        max_length=16,
        choices=MessageRole.choices,
        verbose_name=_("role"),
    )
    content = models.TextField(
        verbose_name=_("content"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    class Meta:
        ordering = ["conversation", "sequence"]
        unique_together = [("conversation", "sequence")]
        verbose_name = _("conversation message")
        verbose_name_plural = _("conversation messages")

    def __str__(self) -> str:
        return f"{self.conversation_id}#{self.sequence} {self.role}"


class SourceEvidence(models.Model):
    """Retrieval evidence attached to an assistant response (SPEC-005 §31–32).

    Foreign keys use SET_NULL so Knowledge Base evolution does not erase
    conversation history.
    """

    message = models.ForeignKey(
        ConversationMessage,
        on_delete=models.CASCADE,
        related_name="source_evidence",
        verbose_name=_("assistant message"),
    )
    document = models.ForeignKey(
        "knowledge.KnowledgeDocument",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("knowledge document"),
    )
    chunk = models.ForeignKey(
        "knowledge.KnowledgeChunk",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("knowledge chunk"),
    )
    rank = models.PositiveIntegerField(
        verbose_name=_("retrieval rank"),
    )
    distance = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("retrieval distance"),
    )
    document_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("document title snapshot"),
    )
    document_slug = models.SlugField(
        max_length=200,
        blank=True,
        verbose_name=_("document slug snapshot"),
    )
    document_language = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_("document language snapshot"),
    )
    document_category = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("document category snapshot"),
    )
    chunk_content = models.TextField(
        blank=True,
        verbose_name=_("chunk content snapshot"),
    )
    retrieved_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("retrieved at"),
    )

    class Meta:
        ordering = ["message", "rank"]
        verbose_name = _("source evidence")
        verbose_name_plural = _("source evidence")

    def __str__(self) -> str:
        return f"{self.message_id} rank={self.rank}"
