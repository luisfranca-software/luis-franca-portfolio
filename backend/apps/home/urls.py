"""URL configuration for the Home module.

Governing documents: SPEC-001 (SPEC-001-REQ-003), ARCH-001 (12.1).
"""

from django.urls import path

from apps.home import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]
