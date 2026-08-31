"""Integration tests for Release 2 Django Administration foundation.

Governing documents: ARCH-001 (17.9), ADR-001 (Release 2 — Platform Evolution).
"""

from __future__ import annotations

import pytest
from django.contrib.auth.models import User
from django.test import Client

from apps.contact.models import CommunicationType, ContactRequest

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_user() -> User:
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.test",
        password="admin-password-123",
    )


@pytest.fixture
def staff_user() -> User:
    return User.objects.create_user(
        username="staff",
        email="staff@example.test",
        password="staff-password-123",
        is_staff=True,
    )


@pytest.fixture
def regular_user() -> User:
    return User.objects.create_user(
        username="regular",
        email="regular@example.test",
        password="regular-password-123",
    )


@pytest.fixture
def contact_request() -> ContactRequest:
    return ContactRequest.objects.create(
        full_name="Ana Souza",
        email="ana@example.test",
        subject="Hello",
        message="Message body",
        communication_type=CommunicationType.CONTACT,
    )


class TestAdminAuthenticationBoundary:
    def test_anonymous_admin_request_redirects_to_login(self) -> None:
        response = Client().get("/admin/")

        assert response.status_code == 302
        assert response.url.startswith("/admin/login/")

    def test_regular_user_cannot_access_admin(self, regular_user) -> None:
        client = Client()
        assert client.login(username="regular", password="regular-password-123") is True

        response = client.get("/admin/")

        assert response.status_code == 302
        assert response.url.startswith("/admin/login/")

    def test_staff_user_can_access_admin(self, staff_user) -> None:
        client = Client()
        assert client.login(username="staff", password="staff-password-123") is True

        response = client.get("/admin/")

        assert response.status_code == 200
        assert b"Django administration" in response.content

    def test_superuser_can_access_admin(self, admin_user) -> None:
        client = Client()
        assert client.login(username="admin", password="admin-password-123") is True

        response = client.get("/admin/")

        assert response.status_code == 200
        assert b"Django administration" in response.content


class TestAdminUserManagement:
    def test_user_changelist_available_to_superuser(self, admin_user) -> None:
        client = Client()
        client.login(username="admin", password="admin-password-123")

        response = client.get("/admin/auth/user/")

        assert response.status_code == 200
        assert b"Select user to change" in response.content

    def test_group_changelist_available_to_superuser(self, admin_user) -> None:
        client = Client()
        client.login(username="admin", password="admin-password-123")

        response = client.get("/admin/auth/group/")

        assert response.status_code == 200
        assert b"Select group to change" in response.content


class TestAdminCsrfProtection:
    def test_admin_login_rejects_post_without_csrf_token(self) -> None:
        client = Client(enforce_csrf_checks=True)
        response = client.post("/admin/login/", {"username": "x", "password": "y"})

        assert response.status_code == 403


class TestContactRequestAdmin:
    def test_contact_request_changelist_is_read_only_for_superuser(
        self, admin_user, contact_request
    ) -> None:
        client = Client()
        client.login(username="admin", password="admin-password-123")

        response = client.get("/admin/contact/contactrequest/")

        assert response.status_code == 200
        content = response.content.decode()
        assert contact_request.email in content
        assert "Add contact request" not in content

    def test_contact_request_detail_is_read_only_for_superuser(
        self, admin_user, contact_request
    ) -> None:
        client = Client()
        client.login(username="admin", password="admin-password-123")

        response = client.get(f"/admin/contact/contactrequest/{contact_request.pk}/change/")

        assert response.status_code == 200
        content = response.content.decode()
        assert contact_request.email in content
        # Read-only forms do not expose a save button.
        assert "Save" not in content

    def test_contact_request_cannot_be_deleted_via_admin(self, admin_user, contact_request) -> None:
        client = Client()
        client.login(username="admin", password="admin-password-123")

        response = client.post(f"/admin/contact/contactrequest/{contact_request.pk}/delete/")

        assert response.status_code == 403
        assert ContactRequest.objects.filter(pk=contact_request.pk).exists() is True

    def test_contact_request_staff_without_permission_cannot_view_changelist(
        self, staff_user, contact_request
    ) -> None:
        client = Client()
        client.login(username="staff", password="staff-password-123")

        response = client.get("/admin/contact/contactrequest/")

        assert response.status_code == 403
