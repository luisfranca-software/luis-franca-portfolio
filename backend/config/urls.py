"""Root URL configuration for the config project.

Product URLs are wired from their respective Feature Specifications.
"""

from django.urls import include, path

urlpatterns = [
    path("contact/", include("apps.contact.urls")),
]
