"""Bootstrap-level settings sanity check.

This is engineering-foundation verification only; no business behavior exists
at this phase.
"""

from django.apps import apps
from django.conf import settings

import config.settings.development as development


def test_development_settings_are_loaded() -> None:
    assert settings.SETTINGS_MODULE == "config.settings.development"
    assert development.DEBUG is True
    assert development.USE_I18N is True
    assert development.USE_TZ is True


def test_development_settings_always_allow_local_hosts() -> None:
    assert "localhost" in development.ALLOWED_HOSTS
    assert "127.0.0.1" in development.ALLOWED_HOSTS


def test_approved_app_modules_are_installed() -> None:
    approved_modules = {
        "apps.core",
        "apps.home",
        "apps.about",
        "apps.skills",
        "apps.experience",
        "apps.portfolio",
        "apps.common",
    }
    installed_modules = {config.name for config in apps.get_app_configs()}
    assert approved_modules.issubset(installed_modules)
