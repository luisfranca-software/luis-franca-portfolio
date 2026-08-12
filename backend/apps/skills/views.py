"""Skills view.

Governing documents: SPEC-001 (SPEC-001-REQ-005), ARCH-001 (12.1).
"""

from typing import Any

from django.views.generic import TemplateView

from apps.skills.skills import SKILL_GROUPS


class SkillsView(TemplateView):
    """Skills section presenting the approved professional technology stack."""

    template_name = "skills/skills.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["skill_groups"] = SKILL_GROUPS
        return context
