"""Root URL configuration for the config project.

Product URLs are wired from their respective Feature Specifications.

The root path serves the Release 1 landing experience: until the SPEC-001 Home
phase is implemented, ``/`` presents the Portfolio module so the deployed site
never 404s at its entry point (SPEC-001-REQ-001, SPEC-001-REQ-003).
"""

from django.urls import include, path

from apps.portfolio.views import PortfolioView

urlpatterns = [
    path("", PortfolioView.as_view(), name="home"),
    path("portfolio/", include("apps.portfolio.urls")),
    path("contact/", include("apps.contact.urls")),
]
