"""Shared presentation configuration for the Common (shared platform) module.

Governing documents: ARCH-001 (14.6, 16.3), ADR-004.
"""

from django.conf import settings


def public_contact_links(request):
    """Expose configured public professional links to all templates.

    External professional links operate as configured outbound links
    (ARCH-001 16.3); values originate from environment configuration.
    """

    return {"contact_links": settings.CONTACT_LINKS}
