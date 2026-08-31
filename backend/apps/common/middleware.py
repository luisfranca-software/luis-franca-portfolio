"""Shared platform middleware for the Common module.

Governing documents: ARCH-001 (14.6), ADR-001 (Release 1.1 analytics).
"""

from __future__ import annotations

import logging

from django.conf import settings

from apps.common.models import AnalyticsEvent

logger = logging.getLogger(__name__)


class AnalyticsMiddleware:
    """Record essential server-side analytics events.

    Page views are captured automatically for successful GET requests to
    application pages. Other event types are recorded explicitly by views or
    client-side event tracking. Analytics can be disabled with the
    ``ANALYTICS_ENABLED`` setting.

    Analytics persistence failures are non-critical and must never break the
    original application response.
    """

    _IGNORED_PATH_PREFIXES = (
        "/static/",
        "/media/",
        "/admin/",
        "/i18n/",
        "/analytics/",
        "/sitemap.xml",
        "/robots.txt",
    )

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            self._maybe_record_page_view(request, response)
        except Exception:
            # Analytics are non-critical; any analytics-related failure must
            # not alter the application response.
            logger.exception("Failed to record page view analytics event")
        return response

    def _maybe_record_page_view(self, request, response) -> None:
        if not getattr(settings, "ANALYTICS_ENABLED", True):
            return
        if request.method != "GET":
            return
        if response.status_code != 200:
            return
        path = request.path_info
        if any(path.startswith(prefix) for prefix in self._IGNORED_PATH_PREFIXES):
            return
        AnalyticsEvent.record(
            event_type=AnalyticsEvent.EventType.PAGE_VIEW,
            request=request,
            path=path,
        )
