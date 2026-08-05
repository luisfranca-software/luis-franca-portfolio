"""Root URL configuration for the config project.

Only bootstrap URL wiring is defined at this phase. Product URLs are
implemented by their respective Feature Specifications.
"""

from django.urls import URLPattern

urlpatterns: list[URLPattern] = []
