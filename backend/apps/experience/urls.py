"""URL configuration for the Experience module.

Governing documents: SPEC-001 (SPEC-001-REQ-006), ARCH-001 (12.1).
"""

from django.urls import path

from apps.experience import views

app_name = "experience"

urlpatterns = [
    path("", views.ExperienceView.as_view(), name="experience"),
]
