"""Integration tests for Knowledge Base persistence, indexing, and retrieval.

Governing documents: SPEC-004 §53.
"""

from __future__ import annotations

import pytest
from django.db import IntegrityError

from apps.knowledge.integrations.fake_embedding_provider import FakeEmbeddingProvider
from apps.knowledge.models import (
    Category,
    IndexingStatus,
    KnowledgeChunk,
    KnowledgeDocument,
    Language,
)
from apps.knowledge.services.embedding_provider import EmbeddingError
from apps.knowledge.services.indexing import IndexingService
from apps.knowledge.services.retrieval import RetrievalService


@pytest.mark.django_db
class TestKnowledgePersistence:
    """KB-IT-001 through KB-IT-005 persistence and relationship tests."""

    def test_knowledge_document_persistence(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Document",
            slug="doc-one",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content here.",
        )
        assert doc.pk is not None
        assert doc.indexing_status == IndexingStatus.PENDING

    def test_knowledge_chunk_persistence(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Document",
            slug="doc-chunk",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content here.",
        )
        chunk = KnowledgeChunk.objects.create(
            document=doc,
            sequence=0,
            content="Chunk content",
            embedding=[0.1] * 1024,
        )
        assert chunk.pk is not None
        assert chunk.document == doc

    def test_vector_1024_persistence(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Document",
            slug="doc-vector",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content here.",
        )
        embedding = [0.01] * 1024
        chunk = KnowledgeChunk.objects.create(
            document=doc,
            sequence=0,
            content="Chunk",
            embedding=embedding,
        )
        chunk.refresh_from_db()
        assert len(chunk.embedding) == 1024

    def test_document_chunk_relationship(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Document",
            slug="doc-rel",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content here.",
        )
        KnowledgeChunk.objects.create(
            document=doc,
            sequence=0,
            content="Chunk one",
            embedding=[0.1] * 1024,
        )
        assert doc.chunks.count() == 1

    def test_document_sequence_uniqueness(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Document",
            slug="doc-unique",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content here.",
        )
        KnowledgeChunk.objects.create(
            document=doc,
            sequence=0,
            content="Chunk one",
            embedding=[0.1] * 1024,
        )
        with pytest.raises(IntegrityError):
            KnowledgeChunk.objects.create(
                document=doc,
                sequence=0,
                content="Chunk two",
                embedding=[0.2] * 1024,
            )


@pytest.mark.django_db
class TestVectorRetrieval:
    """KB-IT-006 through KB-IT-011 retrieval tests."""

    def _index_document(self, **kwargs) -> KnowledgeDocument:
        doc = KnowledgeDocument.objects.create(**kwargs)
        IndexingService(FakeEmbeddingProvider()).index_document(doc)
        doc.refresh_from_db()
        return doc

    def test_cosine_ordering(self) -> None:
        doc = self._index_document(
            title="Python Backend",
            slug="python-backend",
            language=Language.EN,
            category=Category.SKILL,
            content="Python backend development with Django and automated testing.",
        )
        service = RetrievalService(FakeEmbeddingProvider())
        results = service.retrieve("python backend", language="en")
        assert any(r.document_id == doc.pk for r in results)

    def test_active_filtering(self) -> None:
        doc = self._index_document(
            title="Active",
            slug="active-doc",
            language=Language.EN,
            category=Category.GENERAL,
            content="This document is active and retrievable.",
        )
        service = RetrievalService(FakeEmbeddingProvider())
        results = service.retrieve("active retrievable", language="en")
        assert any(r.document_id == doc.pk for r in results)

    def test_inactive_exclusion(self) -> None:
        doc = self._index_document(
            title="Inactive",
            slug="inactive-doc",
            language=Language.EN,
            category=Category.GENERAL,
            content="This document is inactive and should not be retrieved.",
        )
        doc.is_active = False
        doc.save()
        service = RetrievalService(FakeEmbeddingProvider())
        results = service.retrieve("inactive should not", language="en")
        assert not any(r.document_id == doc.pk for r in results)

    def test_language_filtering(self) -> None:
        en_doc = self._index_document(
            title="English Only",
            slug="en-doc",
            language=Language.EN,
            category=Category.GENERAL,
            content="English content about software engineering.",
        )
        self._index_document(
            title="Portuguese Only",
            slug="pt-doc",
            language=Language.PT_BR,
            category=Category.GENERAL,
            content="Conteúdo em português sobre engenharia de software.",
        )
        service = RetrievalService(FakeEmbeddingProvider())
        results = service.retrieve("software engineering", language="en")
        assert any(r.document_id == en_doc.pk for r in results)
        assert all(r.language == "en" for r in results)

    def test_category_filtering(self) -> None:
        skill_doc = self._index_document(
            title="Python Skill",
            slug="python-skill",
            language=Language.EN,
            category=Category.SKILL,
            content="Python programming skill for backend systems.",
        )
        self._index_document(
            title="Project",
            slug="project-doc",
            language=Language.EN,
            category=Category.PROJECT,
            content="Project description.",
        )
        service = RetrievalService(FakeEmbeddingProvider())
        results = service.retrieve("python", language="en", category="SKILL")
        assert all(r.category == "SKILL" for r in results)
        assert any(r.document_id == skill_doc.pk for r in results)

    def test_top_k_limit(self) -> None:
        for index in range(10):
            self._index_document(
                title=f"Doc {index}",
                slug=f"topk-doc-{index}",
                language=Language.EN,
                category=Category.GENERAL,
                content=f"Document number {index} about testing retrieval limits.",
            )
        service = RetrievalService(FakeEmbeddingProvider())
        results = service.retrieve("testing retrieval", language="en", top_k=3)
        assert len(results) == 3


@pytest.mark.django_db
class TestIndexingLifecycle:
    """KB-IT-012 through KB-IT-015 indexing lifecycle tests."""

    def test_successful_indexing_produces_indexed_state(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Document",
            slug="lifecycle-success",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content to index successfully.",
        )
        IndexingService(FakeEmbeddingProvider()).index_document(doc)
        doc.refresh_from_db()
        assert doc.indexing_status == IndexingStatus.INDEXED
        assert doc.chunks.count() >= 1
        assert doc.embedding_model != ""
        assert doc.indexed_at is not None

    def test_failed_initial_indexing_not_false_indexed(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Document",
            slug="lifecycle-fail",
            language=Language.EN,
            category=Category.GENERAL,
            content=FakeEmbeddingProvider.failure_text(),
        )
        with pytest.raises(EmbeddingError):
            IndexingService(FakeEmbeddingProvider()).index_document(doc)
        doc.refresh_from_db()
        assert doc.indexing_status == IndexingStatus.FAILED
        assert doc.chunks.count() == 0

    def test_successful_reindex_atomically_replaces_chunks(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Document",
            slug="reindex-success",
            language=Language.EN,
            category=Category.GENERAL,
            content="Original content for indexing.",
        )
        service = IndexingService(FakeEmbeddingProvider())
        service.index_document(doc)
        original_chunk_pks = set(doc.chunks.values_list("pk", flat=True))

        doc.content = "Updated content after editing."
        doc.save()
        service.index_document(doc)
        doc.refresh_from_db()

        new_chunk_pks = set(doc.chunks.values_list("pk", flat=True))
        assert doc.indexing_status == IndexingStatus.INDEXED
        assert not original_chunk_pks & new_chunk_pks
        assert doc.chunks.count() >= 1

    def test_failed_reindex_preserves_last_valid_chunks(self) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Document",
            slug="reindex-fail",
            language=Language.EN,
            category=Category.GENERAL,
            content="Original content for indexing.",
        )
        service = IndexingService(FakeEmbeddingProvider())
        service.index_document(doc)
        original_chunk_pks = set(doc.chunks.values_list("pk", flat=True))
        assert original_chunk_pks

        doc.content = FakeEmbeddingProvider.failure_text()
        doc.save()
        with pytest.raises(EmbeddingError):
            service.index_document(doc)
        doc.refresh_from_db()

        current_chunk_pks = set(doc.chunks.values_list("pk", flat=True))
        assert doc.indexing_status == IndexingStatus.FAILED
        assert current_chunk_pks == original_chunk_pks


@pytest.mark.django_db
class TestRetrievalAcceptanceDataset:
    """Retrieval acceptance validation using a controlled dataset."""

    def _index(self, **kwargs) -> KnowledgeDocument:
        doc = KnowledgeDocument.objects.create(**kwargs)
        IndexingService(FakeEmbeddingProvider()).index_document(doc)
        return doc

    def test_acceptance_corpus(self) -> None:
        en_skill = self._index(
            title="Python Backend Engineering",
            slug="python-backend-engineering",
            language=Language.EN,
            category=Category.SKILL,
            content=(
                "Luís França builds production-ready Python backend systems using "
                "Django, automated testing, and continuous integration. He designs "
                "maintainable APIs and relational data models for professional "
                "software projects."
            ),
        )
        en_project = self._index(
            title="Portfolio Platform",
            slug="portfolio-platform",
            language=Language.EN,
            category=Category.PROJECT,
            content=(
                "The Site Portfolio is a Django project showcasing professional "
                "experience, skills, and selected engineering work with responsive "
                "design and internationalization."
            ),
        )
        pt_profile = self._index(
            title="Perfil Profissional",
            slug="perfil-profissional",
            language=Language.PT_BR,
            category=Category.PROFILE,
            content=(
                "Luís França é engenheiro de software especializado em desenvolvimento "
                "backend Python, automação e aplicações de IA/LLM. Ele entrega software "
                "manutenível e pronto para produção."
            ),
        )
        inactive = self._index(
            title="Draft Content",
            slug="draft-content",
            language=Language.EN,
            category=Category.GENERAL,
            content="Draft content about software engineering practices.",
        )
        inactive.is_active = False
        inactive.save()

        service = RetrievalService(FakeEmbeddingProvider())

        en_results = service.retrieve("python backend systems", language="en")
        assert any(r.document_id == en_skill.pk for r in en_results)
        assert all(r.language == "en" for r in en_results)
        assert not any(r.document_id == inactive.pk for r in en_results)

        pt_results = service.retrieve("engenheiro de software backend", language="pt-br")
        assert any(r.document_id == pt_profile.pk for r in pt_results)
        assert all(r.language == "pt-br" for r in pt_results)

        category_results = service.retrieve("portfolio", language="en", category="PROJECT")
        assert any(r.document_id == en_project.pk for r in category_results)
        assert all(r.category == "PROJECT" for r in category_results)

        limited = service.retrieve("software", language="en", top_k=2)
        assert len(limited) <= 2


@pytest.mark.django_db
class TestRetrievalInputValidation:
    """RetrievalService must reject unsupported controlled metadata."""

    def _index(self, **kwargs) -> KnowledgeDocument:
        doc = KnowledgeDocument.objects.create(**kwargs)
        IndexingService(FakeEmbeddingProvider()).index_document(doc)
        return doc

    def test_unsupported_language_rejected(self) -> None:
        self._index(
            title="Doc",
            slug="lang-validation",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content.",
        )
        service = RetrievalService(FakeEmbeddingProvider())
        with pytest.raises(ValueError, match="Unsupported language"):
            service.retrieve("content", language="zz")

    def test_unsupported_category_rejected(self) -> None:
        self._index(
            title="Doc",
            slug="cat-validation",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content.",
        )
        service = RetrievalService(FakeEmbeddingProvider())
        with pytest.raises(ValueError, match="Unsupported category"):
            service.retrieve("content", language="en", category="UNKNOWN")

    def test_top_k_bounded(self) -> None:
        self._index(
            title="Doc",
            slug="topk-bound",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content.",
        )
        service = RetrievalService(FakeEmbeddingProvider())
        results = service.retrieve("content", language="en", top_k=200)
        assert len(results) <= 100


@pytest.mark.django_db
class TestRetrievalEligibility:
    """Retrieval uses indexed_at as the success marker, not indexing_status."""

    def _index(self, **kwargs) -> KnowledgeDocument:
        doc = KnowledgeDocument.objects.create(**kwargs)
        IndexingService(FakeEmbeddingProvider()).index_document(doc)
        return doc

    def test_edited_document_retrieves_previous_valid_index(self) -> None:
        """Case C: edited source remains retrievable via previous index."""
        doc = self._index(
            title="Python Backend",
            slug="edit-retrieve",
            language=Language.EN,
            category=Category.SKILL,
            content="Python backend development with Django and automated testing.",
        )
        original_chunk_count = doc.chunks.count()
        original_indexed_at = doc.indexed_at
        assert original_chunk_count > 0

        doc.content = "Updated content about cloud infrastructure."
        doc.indexing_status = IndexingStatus.PENDING
        doc.save()

        service = RetrievalService(FakeEmbeddingProvider())
        results = service.retrieve("python backend django", language="en")
        assert any(r.document_id == doc.pk for r in results)
        assert doc.indexed_at == original_indexed_at
        assert doc.chunks.count() == original_chunk_count

    def test_failed_reindex_retrieves_previous_valid_index(self) -> None:
        """Case D: failed reindex preserves and retrieves previous index."""
        doc = self._index(
            title="Python Backend",
            slug="fail-retrieve",
            language=Language.EN,
            category=Category.SKILL,
            content="Python backend development with Django and automated testing.",
        )
        original_chunk_count = doc.chunks.count()
        original_indexed_at = doc.indexed_at

        doc.content = FakeEmbeddingProvider.failure_text()
        doc.save()
        with pytest.raises(EmbeddingError):
            IndexingService(FakeEmbeddingProvider()).index_document(doc)
        doc.refresh_from_db()

        assert doc.indexing_status == IndexingStatus.FAILED
        assert doc.indexed_at == original_indexed_at
        assert doc.chunks.count() == original_chunk_count

        service = RetrievalService(FakeEmbeddingProvider())
        results = service.retrieve("python backend django", language="en")
        assert any(r.document_id == doc.pk for r in results)

    def test_failed_initial_index_not_retrievable(self) -> None:
        """Case E: failed initial index has no retrievable chunks."""
        doc = KnowledgeDocument.objects.create(
            title="Python Backend",
            slug="initial-fail",
            language=Language.EN,
            category=Category.SKILL,
            content=FakeEmbeddingProvider.failure_text(),
        )
        with pytest.raises(EmbeddingError):
            IndexingService(FakeEmbeddingProvider()).index_document(doc)
        doc.refresh_from_db()

        assert doc.indexing_status == IndexingStatus.FAILED
        assert doc.indexed_at is None
        assert doc.chunks.count() == 0

        service = RetrievalService(FakeEmbeddingProvider())
        results = service.retrieve("python backend django", language="en")
        assert not any(r.document_id == doc.pk for r in results)
