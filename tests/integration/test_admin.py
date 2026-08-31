"""Integration tests for Release 2 Django Administration foundation.

Governing documents: ARCH-001 (17.9), ADR-001 (Release 2 — Platform Evolution).
"""

from __future__ import annotations

import re

import pytest
from django.contrib.auth.models import Group, Permission, User
from django.test import Client

from apps.contact.models import CommunicationType, ContactRequest

pytestmark = pytest.mark.django_db


def _csrf_token(response) -> str:
    """Extract the CSRF token from a rendered admin form response."""
    match = re.search(
        r'<input[^>]+name="csrfmiddlewaretoken"[^>]+value="([^"]+)"',
        response.content.decode(),
    )
    assert match is not None, "CSRF token not found in response"
    return match.group(1)


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
        assert response.url.startswith("/admin/login/")  # type: ignore[attr-defined]

    def test_regular_user_cannot_access_admin(self, regular_user) -> None:
        client = Client()
        assert client.login(username="regular", password="regular-password-123") is True

        response = client.get("/admin/")

        assert response.status_code == 302
        assert response.url.startswith("/admin/login/")  # type: ignore[attr-defined]

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


class TestAdminUserOperations:
    def test_superuser_can_access_user_add_surface(self, admin_user) -> None:
        client = Client()
        client.login(username="admin", password="admin-password-123")

        response = client.get("/admin/auth/user/add/")

        assert response.status_code == 200
        assert b"Add user" in response.content

    def test_superuser_can_create_user_via_admin(self, admin_user) -> None:
        client = Client()
        client.login(username="admin", password="admin-password-123")

        add_response = client.get("/admin/auth/user/add/")
        response = client.post(
            "/admin/auth/user/add/",
            {
                "csrfmiddlewaretoken": _csrf_token(add_response),
                "username": "newoperator",
                "password1": "new-operator-pass-456",
                "password2": "new-operator-pass-456",
            },
        )

        assert response.status_code == 302
        user = User.objects.get(username="newoperator")
        assert user.check_password("new-operator-pass-456") is True
        assert user.is_active is True

    def test_superuser_can_edit_user_administrative_fields(self, admin_user, regular_user) -> None:
        client = Client()
        client.login(username="admin", password="admin-password-123")

        change_url = f"/admin/auth/user/{regular_user.pk}/change/"
        change_response = client.get(change_url)
        response = client.post(
            change_url,
            {
                "csrfmiddlewaretoken": _csrf_token(change_response),
                "username": regular_user.username,
                "is_active": "on",
                "is_staff": "on",
                "is_superuser": "",
                "groups": [],
                "user_permissions": [],
                "date_joined_0": regular_user.date_joined.strftime("%Y-%m-%d"),
                "date_joined_1": regular_user.date_joined.strftime("%H:%M:%S"),
            },
        )

        assert response.status_code == 302
        regular_user.refresh_from_db()
        assert regular_user.is_active is True
        assert regular_user.is_staff is True

    def test_superuser_can_deactivate_user(self, admin_user, regular_user) -> None:
        regular_user.is_active = True
        regular_user.save()
        client = Client()
        client.login(username="admin", password="admin-password-123")

        change_url = f"/admin/auth/user/{regular_user.pk}/change/"
        change_response = client.get(change_url)
        response = client.post(
            change_url,
            {
                "csrfmiddlewaretoken": _csrf_token(change_response),
                "username": regular_user.username,
                "is_staff": "",
                "is_superuser": "",
                "groups": [],
                "user_permissions": [],
                "date_joined_0": regular_user.date_joined.strftime("%Y-%m-%d"),
                "date_joined_1": regular_user.date_joined.strftime("%H:%M:%S"),
                # is_active intentionally omitted -> False
            },
        )

        assert response.status_code == 302
        regular_user.refresh_from_db()
        assert regular_user.is_active is False

    def test_superuser_can_assign_and_remove_staff_status(self, admin_user, regular_user) -> None:
        client = Client()
        client.login(username="admin", password="admin-password-123")

        change_url = f"/admin/auth/user/{regular_user.pk}/change/"
        # Assign staff status.
        change_response = client.get(change_url)
        response = client.post(
            change_url,
            {
                "csrfmiddlewaretoken": _csrf_token(change_response),
                "username": regular_user.username,
                "is_active": "on",
                "is_staff": "on",
                "is_superuser": "",
                "groups": [],
                "user_permissions": [],
                "date_joined_0": regular_user.date_joined.strftime("%Y-%m-%d"),
                "date_joined_1": regular_user.date_joined.strftime("%H:%M:%S"),
            },
        )
        assert response.status_code == 302
        regular_user.refresh_from_db()
        assert regular_user.is_staff is True

        # Remove staff status.
        change_response = client.get(change_url)
        response = client.post(
            change_url,
            {
                "csrfmiddlewaretoken": _csrf_token(change_response),
                "username": regular_user.username,
                "is_active": "on",
                "is_staff": "",
                "is_superuser": "",
                "groups": [],
                "user_permissions": [],
                "date_joined_0": regular_user.date_joined.strftime("%Y-%m-%d"),
                "date_joined_1": regular_user.date_joined.strftime("%H:%M:%S"),
            },
        )
        assert response.status_code == 302
        regular_user.refresh_from_db()
        assert regular_user.is_staff is False


class TestAdminGroupAndPermissionOperations:
    def test_superuser_can_create_group_via_admin(self, admin_user) -> None:
        client = Client()
        client.login(username="admin", password="admin-password-123")

        add_response = client.get("/admin/auth/group/add/")
        response = client.post(
            "/admin/auth/group/add/",
            {
                "csrfmiddlewaretoken": _csrf_token(add_response),
                "name": "Editors",
            },
        )

        assert response.status_code == 302
        group = Group.objects.get(name="Editors")
        assert group.name == "Editors"

    def test_superuser_can_assign_permission_to_group_via_admin(self, admin_user) -> None:
        permission = Permission.objects.first()
        assert permission is not None

        client = Client()
        client.login(username="admin", password="admin-password-123")

        add_response = client.get("/admin/auth/group/add/")
        response = client.post(
            "/admin/auth/group/add/",
            {
                "csrfmiddlewaretoken": _csrf_token(add_response),
                "name": "Operators",
                "permissions": [str(permission.pk)],
            },
        )

        assert response.status_code == 302
        group = Group.objects.get(name="Operators")
        assert list(group.permissions.all()) == [permission]

    def test_superuser_can_assign_permission_to_user_via_admin(
        self, admin_user, regular_user
    ) -> None:
        permission = Permission.objects.first()
        assert permission is not None

        client = Client()
        client.login(username="admin", password="admin-password-123")

        change_url = f"/admin/auth/user/{regular_user.pk}/change/"
        change_response = client.get(change_url)
        response = client.post(
            change_url,
            {
                "csrfmiddlewaretoken": _csrf_token(change_response),
                "username": regular_user.username,
                "is_active": "on",
                "is_staff": "",
                "is_superuser": "",
                "groups": [],
                "user_permissions": [str(permission.pk)],
                "date_joined_0": regular_user.date_joined.strftime("%Y-%m-%d"),
                "date_joined_1": regular_user.date_joined.strftime("%H:%M:%S"),
            },
        )

        assert response.status_code == 302
        regular_user.refresh_from_db()
        assert list(regular_user.user_permissions.all()) == [permission]


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
