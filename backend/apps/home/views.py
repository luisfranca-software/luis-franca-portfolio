"""Home view.

Governing documents: SPEC-001 (SPEC-001-REQ-003), ARCH-001 (12.1).
"""

from typing import Any

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Release 1 Home page presenting the approved professional identity.

    Content (name, titles, positioning, CTA) is approved Product Owner input
    rendered through Django's i18n framework.
    """

    template_name = "home/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["full_name"] = "Luís Eduardo Carvalho França"
        context["display_name"] = "Luís França"
        context["titles"] = (
            _("Software Engineer"),
            _("Python Backend Engineer"),
            _("AI/LLM Engineer"),
        )
        context["positioning"] = _(
            "Software engineering focused on Python, backend systems, automation, "
            "and AI, built with specification-driven development, architecture, "
            "automated testing, and production delivery."
        )
        context["cta_label"] = _("Let's Talk")
        context["cta_url"] = reverse_lazy("contact:contact")
        return context
