"""Knowledge Base models for the Knowledge application.

Governing documents: ADR-006, SPEC-004.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from pgvector.django import VectorField


class Language(models.TextChoices):
    """Supported knowledge content languages (SPEC-004 §8)."""

    EN = "en", _("English")
    PT_BR = "pt-br", _("Portuguese (Brazil)")


class Category(models.TextChoices):
    """Controlled knowledge categories (SPEC-004 §8)."""

    PROFILE = "PROFILE", _("Profile")
    EXPERIENCE = "EXPERIENCE", _("Experience")
    SKILL = "SKILL", _("Skill")
    PROJECT = "PROJECT", _("Project")
    ENGINEERING = "ENGINEERING", _("Engineering")
    PROCESS = "PROCESS", _("Process")
    PORTFOLIO = "PORTFOLIO", _("Portfolio")
    GENERAL = "GENERAL", _("General")


class IndexingStatus(models.TextChoices):
    """Indexing lifecycle states (SPEC-004 §19)."""

    PENDING = "pending", _("Pending")
    INDEXING = "indexing", _("Indexing")
    INDEXED = "indexed", _("Indexed")
    FAILED = "failed", _("Failed")


class KnowledgeDocument(models.Model):
    """Administrator-controlled source knowledge (SPEC-004 §7)."""

    title = models.CharField(
        max_length=200,
        verbose_name=_("title"),
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_("slug"),
    )
    language = models.CharField(
        max_length=10,
        choices=Language.choices,
        verbose_name=_("language"),
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        verbose_name=_("category"),
    )
    content = models.TextField(
        verbose_name=_("content"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
    )
    indexing_status = models.CharField(
        max_length=16,
        choices=IndexingStatus.choices,
        default=IndexingStatus.PENDING,
        verbose_name=_("indexing status"),
    )
    index_version = models.PositiveIntegerField(
        default=1,
        verbose_name=_("index version"),
    )
    embedding_model = models.CharField(
        max_length=128,
        blank=True,
        verbose_name=_("embedding model"),
    )
    indexed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("indexed at"),
    )
    last_index_error = models.TextField(
        blank=True,
        verbose_name=_("last index error"),
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
        ordering = ["-updated_at", "title"]
        verbose_name = _("knowledge document")
        verbose_name_plural = _("knowledge documents")

    def __str__(self) -> str:
        return f"{self.title} ({self.language})"

    def clean(self) -> None:
        super().clean()
        if not self.title or not self.title.strip():
            raise ValidationError({"title": _("Title is required.")})
        if not self.content or not self.content.strip():
            raise ValidationError({"content": _("Content is required.")})


class KnowledgeChunk(models.Model):
    """System-derived retrievable segment (SPEC-004 §10)."""

    document = models.ForeignKey(
        KnowledgeDocument,
        on_delete=models.CASCADE,
        related_name="chunks",
        verbose_name=_("document"),
    )
    sequence = models.PositiveIntegerField(
        verbose_name=_("sequence"),
    )
    content = models.TextField(
        verbose_name=_("content"),
    )
    embedding = VectorField(
        dimensions=1024,
        verbose_name=_("embedding"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    class Meta:
        ordering = ["document", "sequence"]
        unique_together = [("document", "sequence")]
        verbose_name = _("knowledge chunk")
        verbose_name_plural = _("knowledge chunks")

    def __str__(self) -> str:
        return f"{self.document.slug}#{self.sequence}"
