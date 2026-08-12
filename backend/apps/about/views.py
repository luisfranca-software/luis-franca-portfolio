"""About view.

Governing documents: SPEC-001 (SPEC-001-REQ-004), ARCH-001 (12.1).
"""

from django.views.generic import TemplateView


class AboutView(TemplateView):
    """About section presenting the approved professional summary."""

    template_name = "about/about.html"
