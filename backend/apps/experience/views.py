"""Experience view.

Governing documents: SPEC-001 (SPEC-001-REQ-006), ARCH-001 (12.1).
"""

from typing import Any

from django.views.generic import TemplateView


class ExperienceView(TemplateView):
    """Experience section presenting the approved career summary.

    The approved presentation model is a concise career narrative; individual
    chronological roles are not required for Release 1.
    """

    template_name = "experience/experience.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["education"] = (
            "Software Engineering — In progress",
            "Building Construction Technician",
        )
        return context
