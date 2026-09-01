"""IA Jujuju public HTTP boundary.

Governing documents: ADR-007 §19; SPEC-005 §33–36.
"""

from __future__ import annotations

import logging
from typing import Any

from django.http import HttpResponseNotAllowed
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView

from apps.assistant.models import Conversation
from apps.assistant.services.orchestration import AssistantService

logger = logging.getLogger(__name__)


class AssistantPanelView(TemplateView):
    """Render the IA Jujuju interaction panel."""

    template_name = "assistant/panel.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        conversation_id = kwargs.get("conversation_id")
        messages: list[Any] = []
        if conversation_id:
            try:
                conversation = Conversation.objects.get(
                    pk=conversation_id,
                    session_key=self.request.session.session_key,
                )
                messages = list(
                    conversation.messages.select_related("conversation").order_by("sequence")
                )
            except Conversation.DoesNotExist:
                logger.warning(
                    "Assistant panel requested unknown or unauthorized conversation %s",
                    conversation_id,
                )
        context["assistant_messages"] = messages
        context["conversation_id"] = conversation_id
        return context


class AskView(View):
    """Handle a question submission and return a server-rendered partial."""

    http_method_names = ["post", "head", "options"]

    def post(self, request, *args, **kwargs):
        question = request.POST.get("question", "")
        language = request.LANGUAGE_CODE or "en"
        if language.lower().startswith("pt"):
            language = "pt-br"
        else:
            language = "en"

        raw_conversation_id = request.POST.get("conversation_id")
        conversation_id: int | None | str = None
        if raw_conversation_id:
            try:
                conversation_id = int(raw_conversation_id)
            except (TypeError, ValueError):
                conversation_id = raw_conversation_id

        service = AssistantService()
        result = service.ask(request, question, language, conversation_id)

        is_htmx = request.headers.get("HX-Request") == "true"
        template = "assistant/partials/exchange.html" if is_htmx else "assistant/ask_result.html"

        context = {
            "result": result,
            "question": question.strip(),
            "conversation_id": result.conversation_id,
        }

        if not result.success:
            if result.error_code in ("invalid_question", "invalid_conversation"):
                status = 422
            else:
                status = 200
            return TemplateResponse(request, template, context, status=status)

        return TemplateResponse(request, template, context)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
