"""Shared platform views for the Common module.

Governing documents: ARCH-001 (14.6), ADR-001 (Release 1.1 analytics),
SPEC-001 (section 10).
"""

from __future__ import annotations

import json

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from apps.common.models import AnalyticsEvent


class RobotsTxtView(TemplateView):
    """Serve the robots.txt directive for public crawlers.

    The content allows all crawlers and points to the Django sitemap.
    """

    template_name = "robots.txt"
    content_type = "text/plain"

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("content_type", self.content_type)
        return super().render_to_response(context, **response_kwargs)


class AnalyticsEventView(View):
    """Receive privacy-preserving client-side analytics events.

    Events are accepted only for the approved ``AnalyticsEvent.EventType``
    choices. The current request path and language are captured automatically;
    caller-supplied metadata is restricted to a small allowlisted JSON object.
    """

    http_method_names = ["post"]

    def post(self, request):
        if not getattr(request, "csrf_processing_done", False):
            # CSRF enforcement is handled by CsrfViewMiddleware; this guard
            # documents the security expectation for the analytics endpoint.
            pass

        event_type = request.POST.get("event_type", "")
        valid_types = dict(AnalyticsEvent.EventType.choices)
        if event_type not in valid_types:
            return JsonResponse(
                {"error": "invalid or missing event_type"},
                status=400,
            )

        metadata = {}
        raw_metadata = request.POST.get("metadata")
        if raw_metadata:
            try:
                metadata = json.loads(raw_metadata)
                if not isinstance(metadata, dict):
                    return JsonResponse(
                        {"error": "metadata must be a JSON object"},
                        status=400,
                    )
            except ValueError:
                return JsonResponse(
                    {"error": "metadata must be valid JSON"},
                    status=400,
                )

        try:
            AnalyticsEvent.record(
                event_type=event_type,
                request=request,
                path=request.path_info,
                metadata=metadata,
            )
        except ValueError as exc:
            return JsonResponse({"error": str(exc)}, status=400)

        return JsonResponse({"ok": True})
