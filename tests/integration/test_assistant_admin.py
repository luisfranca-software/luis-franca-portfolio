"""Django Admin tests for IA Jujuju conversation data.

Governing documents: SPEC-005 §58.
"""

from __future__ import annotations

import pytest
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from django.urls import reverse

from apps.assistant.models import (
    Conversation,
    ConversationMessage,
    ConversationStatus,
    MessageRole,
    SourceEvidence,
)


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
    content_type = ContentType.objects.get_for_model(Conversation)
    view_permission = Permission.objects.get(
        codename="view_conversation",
        content_type=content_type,
    )
    user.user_permissions.add(view_permission)
    return user


@pytest.fixture
def conversation(db):
    return Conversation.objects.create(
        session_key="test-session",
        language="en",
        status=ConversationStatus.ACTIVE,
    )


@pytest.fixture
def assistant_message(conversation):
    return ConversationMessage.objects.create(
        conversation=conversation,
        sequence=1,
        role=MessageRole.ASSISTANT,
        content="Test answer",
    )


@pytest.fixture
def source_evidence(assistant_message):
    return SourceEvidence.objects.create(
        message=assistant_message,
        rank=1,
        distance=0.25,
        document_title="Doc",
        document_slug="doc",
        document_language="en",
        document_category="GENERAL",
        chunk_content="Chunk content",
    )


@pytest.mark.django_db
class TestAssistantAdminAuthorization:
    def test_anonymous_denied(self) -> None:
        response = Client().get("/admin/assistant/conversation/")
        assert response.status_code == 302

    def test_unauthorized_authenticated_user_denied(self, regular_user) -> None:
        client = Client()
        client.force_login(regular_user)
        response = client.get("/admin/assistant/conversation/")
        assert response.status_code == 302

    def test_staff_without_permission_denied(self, staff_without_permission) -> None:
        client = Client()
        client.force_login(staff_without_permission)
        response = client.get("/admin/assistant/conversation/")
        assert response.status_code in (302, 403)

    def test_staff_with_view_permission_can_access(self, staff_with_view_permission) -> None:
        client = Client()
        client.force_login(staff_with_view_permission)
        response = client.get("/admin/assistant/conversation/")
        assert response.status_code == 200

    def test_superuser_authorized(self, superuser_staff) -> None:
        client = Client()
        client.force_login(superuser_staff)
        response = client.get("/admin/assistant/conversation/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestAssistantAdminInspection:
    def test_conversation_list_visible(self, superuser_staff, conversation) -> None:
        client = Client()
        client.force_login(superuser_staff)
        response = client.get("/admin/assistant/conversation/")
        assert response.status_code == 200
        content = response.content.decode()
        assert str(conversation.pk) in content
        assert "en" in content

    def test_conversation_detail_has_messages(
        self, superuser_staff, conversation, assistant_message
    ) -> None:
        client = Client()
        client.force_login(superuser_staff)
        change_url = reverse(
            "admin:assistant_conversation_change",
            args=[conversation.pk],
        )
        response = client.get(change_url)
        assert response.status_code == 200
        content = response.content.decode()
        assert assistant_message.content in content

    def test_message_detail_has_source_evidence(
        self, superuser_staff, assistant_message, source_evidence
    ) -> None:
        client = Client()
        client.force_login(superuser_staff)
        change_url = reverse(
            "admin:assistant_conversationmessage_change",
            args=[assistant_message.pk],
        )
        response = client.get(change_url)
        assert response.status_code == 200
        content = response.content.decode()
        assert source_evidence.document_title in content
        assert str(source_evidence.rank) in content


@pytest.mark.django_db
class TestAssistantAdminReadOnly:
    def test_conversation_add_denied(self, superuser_staff) -> None:
        client = Client()
        client.force_login(superuser_staff)
        response = client.get("/admin/assistant/conversation/add/")
        assert response.status_code == 403

    def test_message_add_denied(self, superuser_staff) -> None:
        client = Client()
        client.force_login(superuser_staff)
        response = client.get("/admin/assistant/conversationmessage/add/")
        assert response.status_code == 403

    def test_source_evidence_add_denied(self, superuser_staff) -> None:
        client = Client()
        client.force_login(superuser_staff)
        response = client.get("/admin/assistant/sourceevidence/add/")
        assert response.status_code == 403

    def test_message_change_form_is_readonly(self, superuser_staff, assistant_message) -> None:
        client = Client()
        client.force_login(superuser_staff)
        change_url = reverse(
            "admin:assistant_conversationmessage_change",
            args=[assistant_message.pk],
        )
        response = client.get(change_url)
        assert response.status_code == 200
        content = response.content.decode()
        assert 'id="id_content"' not in content or "readonly" in content

    def test_source_evidence_change_form_is_readonly(
        self, superuser_staff, source_evidence
    ) -> None:
        client = Client()
        client.force_login(superuser_staff)
        change_url = reverse(
            "admin:assistant_sourceevidence_change",
            args=[source_evidence.pk],
        )
        response = client.get(change_url)
        assert response.status_code == 200
        content = response.content.decode()
        # Read-only fields are rendered as text, not as editable inputs.
        assert 'id="id_chunk_content"' not in content or "readonly" in content
