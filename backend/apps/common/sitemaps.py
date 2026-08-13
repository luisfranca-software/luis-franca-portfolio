"""Django sitemap configuration for public Release 1 pages.

Governing documents: PB-001 (14.1 Visibility), SPEC-001 (section 10).
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static, public Release 1 pages.

    The Product Brief (PB-001, section 14.1) lists Sitemap as a Release 1
    Visibility capability. SPEC-001 (section 10) requires sitemap
    compatibility as part of the SEO foundation.
    """

    changefreq = "monthly"
    priority = 0.5

    def items(self) -> list[str]:
        return [
            "home:home",
            "about:about",
            "skills:skills",
            "experience:experience",
            "portfolio:portfolio",
            "contact:contact",
        ]

    def location(self, item: str) -> str:
        return reverse(item)
