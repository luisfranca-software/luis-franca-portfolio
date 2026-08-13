"""URL configuration for the About module.

Governing documents: SPEC-001 (SPEC-001-REQ-004), ARCH-001 (12.1).
"""

from django.urls import path

from apps.about import views

app_name = "about"

urlpatterns = [
    path("", views.AboutView.as_view(), name="about"),
]
