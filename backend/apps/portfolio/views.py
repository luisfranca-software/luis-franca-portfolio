"""Portfolio views.

Governing documents: SPEC-003 (SPEC-003-REQ-001, REQ-002, REQ-007, section 7),
ARCH-001 (12.1, 17.4).
"""

from typing import Any

from django.views.generic import TemplateView

from apps.portfolio.projects import FEATURED_PROJECTS


class PortfolioView(TemplateView):
    """Dedicated Portfolio section presenting the featured projects.

    The project dataset is resolved through a single accessor so that future
    database-backed persistence can replace it without changing the view
    contract (SPEC-003-REQ-007).
    """

    template_name = "portfolio/portfolio.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["projects"] = FEATURED_PROJECTS
        return context
