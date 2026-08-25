#!/usr/bin/env python3
"""Serve Django plus development static assets for local visual evidence."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from wsgiref.simple_server import make_server

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

from django.contrib.staticfiles.handlers import StaticFilesHandler  # noqa: E402
from django.core.wsgi import get_wsgi_application  # noqa: E402


def main() -> None:
    application = StaticFilesHandler(get_wsgi_application())
    with make_server("127.0.0.1", 8000, application) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
