"""URL configuration for the IA Jujuju assistant.

Governing documents: SPEC-005 §33.
"""

from django.urls import path

from apps.assistant import views

app_name = "assistant"

urlpatterns = [
    path("", views.AssistantPanelView.as_view(), name="panel"),
    path("<int:conversation_id>/", views.AssistantPanelView.as_view(), name="panel_conversation"),
    path("ask/", views.AskView.as_view(), name="ask"),
]
