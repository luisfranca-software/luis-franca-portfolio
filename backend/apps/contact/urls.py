"""URL configuration for the Contact module.

Governing documents: SPEC-002, ARCH-001 (12.1).
"""

from django.urls import path

from apps.contact import views

app_name = "contact"

urlpatterns = [
    path("", views.ContactView.as_view(), name="contact"),
    path("success/", views.ContactSuccessView.as_view(), name="success"),
    path("failure/", views.ContactFailureView.as_view(), name="failure"),
]
