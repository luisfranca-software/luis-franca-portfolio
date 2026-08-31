"""Root URL configuration for the config project.

Product URLs are wired from their respective Feature Specifications.

The root path now serves the approved SPEC-001 Home page (SPEC-001-REQ-003);
Portfolio and Contact retain their dedicated routes (SPEC-001-REQ-007,
SPEC-001-REQ-008). Language selection is handled by LocaleMiddleware and the
Django set_language view without prefixing URLs.
"""

from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.common.sitemaps import StaticViewSitemap

SITEMAPS = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("apps.common.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("", include("apps.home.urls")),
    path("about/", include("apps.about.urls")),
    path("skills/", include("apps.skills.urls")),
    path("experience/", include("apps.experience.urls")),
    path("portfolio/", include("apps.portfolio.urls")),
    path("contact/", include("apps.contact.urls")),
]
