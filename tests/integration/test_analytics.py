"""Integration tests for Release 1.1 essential analytics (ADR-001).

Analytics is implemented server-side with data minimization. These tests verify
that page views, explicit events, and Contact success are recorded without
storing PII.
"""

import pytest
from django.test import Client, override_settings

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
        assert event.session_fingerprint == ""

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
            {"event_type": "contact_cta", "path": "/"},
        )

        assert response.status_code == 200
        event = AnalyticsEvent.objects.get()
        assert event.event_type == AnalyticsEvent.EventType.CONTACT_CTA
        assert event.path == "/"

    def test_invalid_event_type_is_rejected(self, analytics_enabled) -> None:
        response = Client().post(
            "/analytics/event/",
            {"event_type": "unknown_event", "path": "/"},
        )

        assert response.status_code == 400
        assert AnalyticsEvent.objects.count() == 0

    def test_metadata_is_stored(self, analytics_enabled) -> None:
        response = Client().post(
            "/analytics/event/",
            {
                "event_type": "project_interaction",
                "path": "/",
                "metadata": '{"project": "enterprise-platform"}',
            },
        )

        assert response.status_code == 200
        event = AnalyticsEvent.objects.get()
        assert event.metadata == {"project": "enterprise-platform"}

    def test_analytics_disabled_returns_ok_without_creating_event(self, settings) -> None:
        settings.ANALYTICS_ENABLED = False
        response = Client().post(
            "/analytics/event/",
            {"event_type": "contact_cta", "path": "/"},
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
