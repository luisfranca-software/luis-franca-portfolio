"""Regression tests for production static asset fingerprinting."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
SITE_PACKAGES = REPO_ROOT / ".venv" / "lib" / "python3.13" / "site-packages"
HOME_TEMPLATE = REPO_ROOT / "frontend" / "templates" / "home" / "home.html"
PRODUCTION_SETTINGS = BACKEND_DIR / "config" / "settings" / "production.py"


def _load_production_settings() -> types.ModuleType:
    namespace: dict[str, object] = {
        "__name__": "config.settings.production",
        "__package__": "config.settings",
    }
    sys.path.insert(0, str(BACKEND_DIR))
    try:
        exec(PRODUCTION_SETTINGS.read_text(encoding="utf-8"), namespace)
    finally:
        sys.path.pop(0)
    module = types.ModuleType("config.settings.production")
    module.__dict__.update(namespace)
    return module


production = _load_production_settings()


def _python_env() -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    paths = [str(BACKEND_DIR), str(SITE_PACKAGES)]
    if existing:
        paths.append(existing)
    env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def _run_static_probe(static_root: Path) -> dict[str, object]:
    script = f"""
import json
from pathlib import Path

from django.conf import settings

STATIC_ROOT = Path({str(static_root)!r})
STATIC_ROOT.mkdir(parents=True, exist_ok=True)

settings.configure(
    SECRET_KEY="test-secret-key",
    DEBUG=False,
    USE_I18N=True,
    USE_TZ=True,
    ROOT_URLCONF=__name__,
    INSTALLED_APPS=["django.contrib.staticfiles"],
    STATIC_URL="/static/",
    STATICFILES_DIRS=[Path({str(REPO_ROOT / "frontend" / "static")!r})],
    STATIC_ROOT=STATIC_ROOT,
    STORAGES={production.STORAGES!r},
    TEMPLATES=[{{"BACKEND": "django.template.backends.django.DjangoTemplates"}}],
)

import django

django.setup()

from django.core.management import call_command
from django.template import Context, Template

call_command("collectstatic", interactive=False, verbosity=0)

manifest = json.loads((STATIC_ROOT / "staticfiles.json").read_text(encoding="utf-8"))
rendered = Template(
    '{{% load static %}}'
    '<link rel="stylesheet" href="{{% static "css/home.css" %}}">'
    '<script src="{{% static "js/assistant.js" %}}" defer></script>'
).render(Context())
hashed_home_css = STATIC_ROOT / manifest["paths"]["css/home.css"]
print(json.dumps({{
    "manifest": manifest,
    "rendered": rendered,
    "hashed_home_css": hashed_home_css.read_text(encoding="utf-8"),
}}))
"""

    result = subprocess.run(
        ["python3", "-c", script],
        check=True,
        capture_output=True,
        text=True,
        env=_python_env(),
        cwd=REPO_ROOT,
    )
    return json.loads(result.stdout)


def test_production_settings_use_manifest_staticfiles_storage() -> None:
    backend = production.STORAGES["staticfiles"]["BACKEND"]

    assert backend == "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    default_backend = production.STORAGES["default"]["BACKEND"]
    assert default_backend == "django.core.files.storage.FileSystemStorage"


def test_production_default_storage_resolves_to_filesystem_storage() -> None:
    script = """
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"

import django

django.setup()

from django.core.files.storage import default_storage

print(default_storage.__class__.__module__ + "." + default_storage.__class__.__name__)
"""

    result = subprocess.run(
        [str(REPO_ROOT / ".venv" / "bin" / "python"), "-c", script],
        check=True,
        capture_output=True,
        text=True,
        cwd=BACKEND_DIR,
        env=_python_env(),
    )

    assert result.stdout.strip() == "django.core.files.storage.filesystem.FileSystemStorage"


def test_home_template_uses_static_storage_without_manual_query_suffix() -> None:
    template = HOME_TEMPLATE.read_text(encoding="utf-8")

    assert "{% static 'css/home.css' %}?v=" not in template
    assert '{% static "css/home.css" %}?v=' not in template
    assert '<link rel="stylesheet" href="{% static \'css/home.css\' %}">' in template


def test_collectstatic_builds_manifest_and_hashes_home_assets(tmp_path: Path) -> None:
    probe = _run_static_probe(tmp_path / "staticfiles")
    manifest_paths = probe["manifest"]["paths"]

    assert manifest_paths["css/home.css"].startswith("css/home.")
    assert manifest_paths["css/home.css"].endswith(".css")
    assert manifest_paths["js/assistant.js"].startswith("js/assistant.")
    assert manifest_paths["js/assistant.js"].endswith(".js")


def test_collectstatic_rewrites_homepage_background_reference_to_hashed_asset(
    tmp_path: Path,
) -> None:
    probe = _run_static_probe(tmp_path / "staticfiles")
    manifest_paths = probe["manifest"]["paths"]
    css = probe["hashed_home_css"]

    assert "../images/background/homepage-background-desktop-02." in css
    assert manifest_paths["images/background/homepage-background-desktop-02.png"] in css
    assert "../images/background/homepage-background-desktop.png" not in css


def test_rendered_home_static_fragment_uses_fingerprinted_urls(tmp_path: Path) -> None:
    probe = _run_static_probe(tmp_path / "staticfiles")
    rendered = probe["rendered"]

    assert re.search(r'href="/static/css/home\.[0-9a-f]{12}\.css"', rendered) is not None
    assert re.search(r'src="/static/js/assistant\.[0-9a-f]{12}\.js"', rendered) is not None
    assert "?v=" not in rendered
