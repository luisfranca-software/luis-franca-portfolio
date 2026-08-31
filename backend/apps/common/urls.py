"""URL configuration for the Common (shared platform) module.

Governing documents: ARCH-001 (14.6), ADR-001 (Release 1.1 analytics).
"""

from django.urls import path

from apps.common.views import AnalyticsEventView, RobotsTxtView

app_name = "common"

urlpatterns = [
    path("robots.txt", RobotsTxtView.as_view(), name="robots_txt"),
    path("analytics/event/", AnalyticsEventView.as_view(), name="analytics_event"),
]
