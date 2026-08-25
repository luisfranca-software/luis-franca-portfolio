"""Home view.

Governing documents: SPEC-001 (SPEC-001-REQ-003), ARCH-001 (12.1).
"""

from typing import Any

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from apps.home.content import ENGINEERING_CAPABILITIES, EVIDENCE_THEMES, PROCESS_STEPS
from apps.portfolio.projects import FEATURED_PROJECTS


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
        context["is_homepage"] = True
        context["engineering_capabilities"] = ENGINEERING_CAPABILITIES
        context["featured_projects"] = FEATURED_PROJECTS
        context["process_steps"] = PROCESS_STEPS
        context["evidence_themes"] = EVIDENCE_THEMES
        context["contact_cta_url"] = reverse_lazy("contact:contact")
        return context
