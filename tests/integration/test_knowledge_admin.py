"""Django Admin tests for the Knowledge application.

Governing documents: SPEC-004 §54.
"""

from __future__ import annotations

import logging

import pytest
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from django.urls import reverse

from apps.knowledge.models import (
    Category,
    IndexingStatus,
    KnowledgeChunk,
    KnowledgeDocument,
    Language,
)
from apps.knowledge.services.embedding_provider import EmbeddingError

INLINE_MANAGEMENT_DATA = {
    "chunks-TOTAL_FORMS": "0",
    "chunks-INITIAL_FORMS": "0",
    "chunks-MIN_NUM_FORMS": "0",
    "chunks-MAX_NUM_FORMS": "1000",
}


@pytest.fixture
def openai_api_key(settings):
    """Provide a dummy OpenAI API key so production provider instantiation succeeds."""
    original = getattr(settings, "OPENAI_API_KEY", "")
    settings.OPENAI_API_KEY = "test-api-key"
    yield
    settings.OPENAI_API_KEY = original


@pytest.fixture
def superuser_staff(db):
    return User.objects.create_user(
        username="staff",
        password="staff-password-123",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        username="regular",
        password="regular-password-123",
        is_staff=False,
        is_superuser=False,
    )


@pytest.fixture
def staff_without_permission(db):
    return User.objects.create_user(
        username="staff-no-perm",
        password="staff-password-123",
        is_staff=True,
        is_superuser=False,
    )


@pytest.fixture
def staff_with_view_permission(db):
    user = User.objects.create_user(
        username="staff-view",
        password="staff-password-123",
        is_staff=True,
        is_superuser=False,
    )
    content_type = ContentType.objects.get_for_model(KnowledgeDocument)
    view_permission = Permission.objects.get(
        codename="view_knowledgedocument",
        content_type=content_type,
    )
    user.user_permissions.add(view_permission)
    return user


@pytest.fixture
def staff_with_chunk_view_permission(db):
    user = User.objects.create_user(
        username="staff-chunk-view",
        password="staff-password-123",
        is_staff=True,
        is_superuser=False,
    )
    content_type = ContentType.objects.get_for_model(KnowledgeChunk)
    view_permission = Permission.objects.get(
        codename="view_knowledgechunk",
        content_type=content_type,
    )
    user.user_permissions.add(view_permission)
    return user


@pytest.fixture
def staff_with_change_permission(db):
    user = User.objects.create_user(
        username="staff-change",
        password="staff-password-123",
        is_staff=True,
        is_superuser=False,
    )
    content_type = ContentType.objects.get_for_model(KnowledgeDocument)
    change_permission = Permission.objects.get(
        codename="change_knowledgedocument",
        content_type=content_type,
    )
    user.user_permissions.add(change_permission)
    return user


@pytest.mark.django_db
class TestKnowledgeAdminAuthorization:
    """KB-ADM-001 through KB-ADM-003 authorization."""

    def test_anonymous_denied(self) -> None:
        response = Client().get("/admin/knowledge/knowledgedocument/")
        assert response.status_code == 302

    def test_unauthorized_authenticated_user_denied(self, regular_user) -> None:
        client = Client()
        client.force_login(regular_user)
        response = client.get("/admin/knowledge/knowledgedocument/")
        assert response.status_code == 302

    def test_staff_without_permission_denied(self, staff_without_permission) -> None:
        client = Client()
        client.force_login(staff_without_permission)
        response = client.get("/admin/knowledge/knowledgedocument/")
        assert response.status_code in (302, 403)

    def test_staff_with_view_permission_can_access(self, staff_with_view_permission) -> None:
        client = Client()
        client.force_login(staff_with_view_permission)
        response = client.get("/admin/knowledge/knowledgedocument/")
        assert response.status_code == 200

    def test_staff_with_change_permission_can_access_change_form(
        self, staff_with_change_permission
    ) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Doc",
            slug="perm-change",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content.",
        )
        client = Client()
        client.force_login(staff_with_change_permission)
        change_url = reverse(
            "admin:knowledge_knowledgedocument_change",
            args=[doc.pk],
        )
        response = client.get(change_url)
        assert response.status_code == 200

    def test_superuser_authorized(self, superuser_staff) -> None:
        client = Client()
        client.force_login(superuser_staff)
        response = client.get("/admin/knowledge/knowledgedocument/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestKnowledgeAdminOperations:
    """KB-ADM-004 through KB-ADM-009 Admin behavior."""

    def test_create_knowledge_document(self, superuser_staff) -> None:
        client = Client()
        client.force_login(superuser_staff)
        add_url = reverse("admin:knowledge_knowledgedocument_add")
        response = client.get(add_url)
        assert response.status_code == 200

        response = client.post(
            add_url,
            {
                "title": "New Document",
                "slug": "new-document",
                "language": "en",
                "category": "GENERAL",
                "content": "Document content here.",
                "is_active": "on",
                **INLINE_MANAGEMENT_DATA,
            },
            follow=True,
        )
        assert response.status_code == 200
        assert KnowledgeDocument.objects.filter(slug="new-document").exists()

    def test_edit_knowledge_document(self, superuser_staff) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Original",
            slug="original-doc",
            language=Language.EN,
            category=Category.GENERAL,
            content="Original content.",
        )
        client = Client()
        client.force_login(superuser_staff)
        change_url = reverse(
            "admin:knowledge_knowledgedocument_change",
            args=[doc.pk],
        )
        response = client.post(
            change_url,
            {
                "title": "Updated",
                "slug": "original-doc",
                "language": "en",
                "category": "GENERAL",
                "content": "Updated content.",
                "is_active": "on",
                **INLINE_MANAGEMENT_DATA,
            },
            follow=True,
        )
        assert response.status_code == 200
        doc.refresh_from_db()
        assert doc.title == "Updated"

    def test_content_edit_preserves_last_successful_index_metadata(self, superuser_staff) -> None:
        """Editing source content marks the document pending but keeps prior metadata."""
        doc = KnowledgeDocument.objects.create(
            title="Doc",
            slug="metadata-preserve",
            language=Language.EN,
            category=Category.GENERAL,
            content="Original content.",
            indexing_status=IndexingStatus.INDEXED,
            embedding_model="text-embedding-3-small",
            indexed_at="2026-01-01T00:00:00Z",
        )
        client = Client()
        client.force_login(superuser_staff)
        change_url = reverse(
            "admin:knowledge_knowledgedocument_change",
            args=[doc.pk],
        )
        response = client.post(
            change_url,
            {
                "title": "Doc",
                "slug": "metadata-preserve",
                "language": "en",
                "category": "GENERAL",
                "content": "Updated content after editing.",
                "is_active": "on",
                **INLINE_MANAGEMENT_DATA,
            },
            follow=True,
        )
        assert response.status_code == 200
        doc.refresh_from_db()
        assert doc.indexing_status == IndexingStatus.PENDING
        assert doc.embedding_model == "text-embedding-3-small"
        assert doc.indexed_at is not None

    def test_activate_deactivate(self, superuser_staff) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Doc",
            slug="active-toggle",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content.",
            is_active=True,
        )
        client = Client()
        client.force_login(superuser_staff)
        change_url = reverse(
            "admin:knowledge_knowledgedocument_change",
            args=[doc.pk],
        )
        response = client.post(
            change_url,
            {
                "title": "Doc",
                "slug": "active-toggle",
                "language": "en",
                "category": "GENERAL",
                "content": "Content.",
                "is_active": "",
                **INLINE_MANAGEMENT_DATA,
            },
            follow=True,
        )
        assert response.status_code == 200
        doc.refresh_from_db()
        assert not doc.is_active

    def test_indexing_status_visible(self, superuser_staff) -> None:
        KnowledgeDocument.objects.create(
            title="Doc",
            slug="status-visible",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content.",
        )
        client = Client()
        client.force_login(superuser_staff)
        response = client.get("/admin/knowledge/knowledgedocument/")
        assert response.status_code == 200
        content = response.content.decode()
        assert "Pending" in content

    def test_reindex_action_uses_indexing_service(
        self, superuser_staff, monkeypatch, openai_api_key
    ) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Doc",
            slug="reindex-action",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content to reindex.",
        )
        called = False

        def fake_index_document(self, document):
            nonlocal called
            called = True
            document.indexing_status = IndexingStatus.INDEXED
            document.save(update_fields=["indexing_status"])

        monkeypatch.setattr(
            "apps.knowledge.services.indexing.IndexingService.index_document",
            fake_index_document,
        )

        client = Client()
        client.force_login(superuser_staff)
        response = client.post(
            "/admin/knowledge/knowledgedocument/",
            {
                "action": "reindex_selected_documents",
                "_selected_action": [str(doc.pk)],
            },
            follow=True,
        )
        assert response.status_code == 200
        assert called

    def test_reindex_action_reports_provider_error_when_key_missing(
        self, superuser_staff, settings
    ) -> None:
        """Missing OPENAI_API_KEY must not silently fall back to fake indexing."""
        settings.OPENAI_API_KEY = ""
        doc = KnowledgeDocument.objects.create(
            title="Doc",
            slug="reindex-no-key",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content to reindex.",
        )
        client = Client()
        client.force_login(superuser_staff)
        response = client.post(
            "/admin/knowledge/knowledgedocument/",
            {
                "action": "reindex_selected_documents",
                "_selected_action": [str(doc.pk)],
            },
            follow=True,
        )
        assert response.status_code == 200
        content = response.content.decode()
        assert "not configured" in content or "unavailable" in content.lower()

    def test_chunk_readonly_in_admin(self, superuser_staff) -> None:
        client = Client()
        client.force_login(superuser_staff)
        response = client.get("/admin/knowledge/knowledgechunk/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestKnowledgeChunkAdminAuthorization:
    """KB-ADM-010 chunk admin is read-only and permission-gated."""

    def test_staff_with_view_permission_can_list_chunks(
        self, staff_with_chunk_view_permission
    ) -> None:
        client = Client()
        client.force_login(staff_with_chunk_view_permission)
        response = client.get("/admin/knowledge/knowledgechunk/")
        assert response.status_code == 200

    def test_staff_without_permission_cannot_list_chunks(self, staff_without_permission) -> None:
        client = Client()
        client.force_login(staff_without_permission)
        response = client.get("/admin/knowledge/knowledgechunk/")
        assert response.status_code in (302, 403)

    def test_chunk_admin_has_no_add_permission(self, superuser_staff) -> None:
        client = Client()
        client.force_login(superuser_staff)
        response = client.get("/admin/knowledge/knowledgechunk/add/")
        assert response.status_code == 403

    def test_chunk_admin_change_form_is_readonly(self, superuser_staff) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Doc",
            slug="chunk-perm",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content.",
        )
        chunk = KnowledgeChunk.objects.create(
            document=doc,
            sequence=0,
            content="Chunk",
            embedding=[0.1] * 1024,
        )
        client = Client()
        client.force_login(superuser_staff)
        change_url = reverse(
            "admin:knowledge_knowledgechunk_change",
            args=[chunk.pk],
        )
        response = client.get(change_url)
        assert response.status_code == 200
        content = response.content.decode()
        assert 'id="id_content"' not in content or "readonly" in content


@pytest.mark.django_db
class TestKnowledgeAdminLogSanitization:
    """Provider/reindex exceptions must be logged by class, not raw text."""

    def test_provider_setup_error_does_not_log_raw_exception_text(
        self, superuser_staff, settings, caplog
    ) -> None:
        settings.OPENAI_API_KEY = ""
        doc = KnowledgeDocument.objects.create(
            title="Doc",
            slug="log-provider-setup",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content to reindex.",
        )
        client = Client()
        client.force_login(superuser_staff)

        with caplog.at_level(logging.WARNING):
            response = client.post(
                "/admin/knowledge/knowledgedocument/",
                {
                    "action": "reindex_selected_documents",
                    "_selected_action": [str(doc.pk)],
                },
                follow=True,
            )

        assert response.status_code == 200
        content = response.content.decode()
        assert "not configured" in content or "unavailable" in content.lower()
        assert "OPENAI_API_KEY" not in caplog.text
        assert "is not configured" not in caplog.text
        assert "EmbeddingError" in caplog.text

    def test_reindex_failure_does_not_log_raw_exception_text(
        self, superuser_staff, monkeypatch, openai_api_key, caplog
    ) -> None:
        doc = KnowledgeDocument.objects.create(
            title="Doc",
            slug="log-reindex-failure",
            language=Language.EN,
            category=Category.GENERAL,
            content="Content to reindex.",
        )

        def fail_indexing(self, document):
            raise EmbeddingError("sensitive provider response body")

        monkeypatch.setattr(
            "apps.knowledge.services.indexing.IndexingService.index_document",
            fail_indexing,
        )

        client = Client()
        client.force_login(superuser_staff)

        with caplog.at_level(logging.WARNING):
            response = client.post(
                "/admin/knowledge/knowledgedocument/",
                {
                    "action": "reindex_selected_documents",
                    "_selected_action": [str(doc.pk)],
                },
                follow=True,
            )

        assert response.status_code == 200
        content = response.content.decode()
        assert "0 document(s), 1 failed" in content
        assert "sensitive provider response body" not in caplog.text
        assert "EmbeddingError" in caplog.text
