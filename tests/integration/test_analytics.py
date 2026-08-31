"""Integration tests for Release 1.1 essential analytics (ADR-001).

Analytics is implemented server-side with data minimization. These tests verify
that page views, explicit events, and Contact success are recorded without
storing PII.
"""

from datetime import timedelta
from unittest import mock

import pytest
from django.core.management import call_command
from django.test import Client, override_settings
from django.utils import timezone

from apps.common.models import AnalyticsEvent
from apps.contact.models import CommunicationType, ContactRequest

pytestmark = pytest.mark.django_db


@pytest.fixture
def analytics_enabled(settings):
    """Enable analytics for a single test."""
    with override_settings(ANALYTICS_ENABLED=True):
        yield


class TestPageViewTracking:
    def test_home_get_creates_page_view_event(self, analytics_enabled) -> None:
        assert AnalyticsEvent.objects.count() == 0
        Client().get("/")

        event = AnalyticsEvent.objects.get()
        assert event.event_type == AnalyticsEvent.EventType.PAGE_VIEW
        assert event.path == "/"
        assert event.language == "en"

    def test_static_requests_do_not_create_events(self, analytics_enabled) -> None:
        # Static files are served by Nginx in production; in development they may
        # be served by Django. Either way, no analytics event is recorded.
        Client().get("/static/css/site.css")
        assert AnalyticsEvent.objects.count() == 0

    def test_sitemap_does_not_create_page_view(self, analytics_enabled) -> None:
        Client().get("/sitemap.xml")
        assert AnalyticsEvent.objects.count() == 0

    def test_robots_txt_does_not_create_page_view(self, analytics_enabled) -> None:
        Client().get("/robots.txt")
        assert AnalyticsEvent.objects.count() == 0

    def test_post_requests_do_not_create_page_view(self, analytics_enabled) -> None:
        Client().post("/contact/", {})
        assert AnalyticsEvent.objects.count() == 0

    def test_non_200_responses_do_not_create_page_view(self, analytics_enabled) -> None:
        Client().get("/nonexistent/")
        assert AnalyticsEvent.objects.count() == 0


class TestEventEndpoint:
    def test_valid_event_is_recorded(self, analytics_enabled) -> None:
        response = Client().post(
            "/analytics/event/",
            {"event_type": "contact_cta"},
        )

        assert response.status_code == 200
        event = AnalyticsEvent.objects.get()
        assert event.event_type == AnalyticsEvent.EventType.CONTACT_CTA
        assert event.path == "/analytics/event/"

    def test_invalid_event_type_is_rejected(self, analytics_enabled) -> None:
        response = Client().post(
            "/analytics/event/",
            {"event_type": "unknown_event"},
        )

        assert response.status_code == 400
        assert AnalyticsEvent.objects.count() == 0

    def test_allowlisted_metadata_is_stored(self, analytics_enabled) -> None:
        response = Client().post(
            "/analytics/event/",
            {
                "event_type": "project_interaction",
                "metadata": '{"project": "enterprise-platform", "action": "expand"}',
            },
        )

        assert response.status_code == 200
        event = AnalyticsEvent.objects.get()
        assert event.metadata == {"project": "enterprise-platform", "action": "expand"}

    def test_unsupported_metadata_keys_are_dropped(self, analytics_enabled) -> None:
        response = Client().post(
            "/analytics/event/",
            {
                "event_type": "project_interaction",
                "metadata": '{"project": "enterprise-platform", "injected": "value"}',
            },
        )

        assert response.status_code == 200
        event = AnalyticsEvent.objects.get()
        assert event.metadata == {"project": "enterprise-platform"}

    def test_metadata_must_be_an_object(self, analytics_enabled) -> None:
        response = Client().post(
            "/analytics/event/",
            {
                "event_type": "project_interaction",
                "metadata": '"string"',
            },
        )

        assert response.status_code == 400
        assert AnalyticsEvent.objects.count() == 0

    def test_invalid_metadata_json_is_rejected(self, analytics_enabled) -> None:
        response = Client().post(
            "/analytics/event/",
            {
                "event_type": "project_interaction",
                "metadata": "not-json",
            },
        )

        assert response.status_code == 400
        assert AnalyticsEvent.objects.count() == 0

    def test_oversized_metadata_value_is_rejected(self, analytics_enabled) -> None:
        response = Client().post(
            "/analytics/event/",
            {
                "event_type": "project_interaction",
                "metadata": '{"project": "%s"}' % ("x" * 200),
            },
        )

        assert response.status_code == 400
        assert AnalyticsEvent.objects.count() == 0

    def test_client_supplied_path_is_ignored(self, analytics_enabled) -> None:
        response = Client().post(
            "/analytics/event/",
            {
                "event_type": "contact_cta",
                "path": "https://evil.example.test/",
            },
        )

        assert response.status_code == 200
        event = AnalyticsEvent.objects.get()
        assert event.path == "/analytics/event/"

    def test_analytics_disabled_returns_ok_without_creating_event(self, settings) -> None:
        settings.ANALYTICS_ENABLED = False
        response = Client().post(
            "/analytics/event/",
            {"event_type": "contact_cta"},
        )

        assert response.status_code == 200
        assert AnalyticsEvent.objects.count() == 0


class TestContactSuccessTracking:
    @pytest.fixture(autouse=True)
    def email_backend(self):
        with override_settings(
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
            DEFAULT_FROM_EMAIL="portfolio@example.test",
            CONTACT_NOTIFICATION_EMAIL="owner@example.test",
        ):
            yield

    def test_contact_success_creates_analytics_event(self, analytics_enabled) -> None:
        response = Client().post(
            "/contact/",
            {
                "full_name": "Ana Souza",
                "email": "ana@example.test",
                "subject": "Hello",
                "message": "Message body",
                "communication_type": CommunicationType.CONTACT,
            },
        )

        assert response.status_code == 302
        assert ContactRequest.objects.count() == 1
        success_event = AnalyticsEvent.objects.get(
            event_type=AnalyticsEvent.EventType.CONTACT_SUCCESS
        )
        assert success_event.path == "/contact/"
        assert success_event.metadata["communication_type"] == CommunicationType.CONTACT

    def test_analytics_failure_does_not_break_contact_submission(self, analytics_enabled) -> None:
        with mock.patch.object(
            AnalyticsEvent.objects, "create", side_effect=RuntimeError("DB down")
        ):
            response = Client().post(
                "/contact/",
                {
                    "full_name": "Ana Souza",
                    "email": "ana@example.test",
                    "subject": "Hello",
                    "message": "Message body",
                    "communication_type": CommunicationType.CONTACT,
                },
            )

        assert response.status_code == 302
        assert ContactRequest.objects.count() == 1


class TestAnalyticsRetention:
    def _create(self, event_type, created_at) -> AnalyticsEvent:
        return AnalyticsEvent.objects.create(
            event_type=event_type,
            path="/",
            language="en",
            created_at=created_at,
        )

    def test_purge_deletes_only_expired_events(self, analytics_enabled) -> None:
        expired = self._create(
            AnalyticsEvent.EventType.PAGE_VIEW,
            timezone.now() - timedelta(days=400),
        )
        recent = self._create(
            AnalyticsEvent.EventType.PAGE_VIEW,
            timezone.now() - timedelta(days=1),
        )

        call_command("purge_analytics_events")

        assert AnalyticsEvent.objects.filter(pk=expired.pk).exists() is False
        assert AnalyticsEvent.objects.filter(pk=recent.pk).exists() is True

    def test_purge_dry_run_does_not_delete(self, analytics_enabled) -> None:
        expired = self._create(
            AnalyticsEvent.EventType.PAGE_VIEW,
            timezone.now() - timedelta(days=400),
        )

        call_command("purge_analytics_events", "--dry-run")

        assert AnalyticsEvent.objects.filter(pk=expired.pk).exists() is True

    def test_purge_respects_days_override(self, analytics_enabled) -> None:
        old = self._create(
            AnalyticsEvent.EventType.PAGE_VIEW,
            timezone.now() - timedelta(days=100),
        )

        call_command("purge_analytics_events", "--days", "365")
        assert AnalyticsEvent.objects.filter(pk=old.pk).exists() is True

        call_command("purge_analytics_events", "--days", "90")
        assert AnalyticsEvent.objects.filter(pk=old.pk).exists() is False

    def test_purge_is_idempotent(self, analytics_enabled) -> None:
        self._create(
            AnalyticsEvent.EventType.PAGE_VIEW,
            timezone.now() - timedelta(days=400),
        )

        call_command("purge_analytics_events")
        call_command("purge_analytics_events")

        assert AnalyticsEvent.objects.count() == 0
