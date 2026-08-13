"""URL configuration for the Skills module.

Governing documents: SPEC-001 (SPEC-001-REQ-005), ARCH-001 (12.1).
"""

from django.urls import path

from apps.skills import views

app_name = "skills"

urlpatterns = [
    path("", views.SkillsView.as_view(), name="skills"),
]
