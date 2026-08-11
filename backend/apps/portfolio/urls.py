"""URL configuration for the Portfolio module.

Governing documents: SPEC-003, ARCH-001 (12.1).
"""

from django.urls import path

from apps.portfolio import views

app_name = "portfolio"

urlpatterns = [
    path("", views.PortfolioView.as_view(), name="portfolio"),
]
