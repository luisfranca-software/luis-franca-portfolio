"""Environment configuration loader.

Loads the repository-root ``.env`` file (when present) into the process
environment and exposes typed accessors used by the settings modules.

Governing documents: ARCH-001 (AR-009), 06-deployment-and-operations.md.
Secrets are never hardcoded; every value originates from the environment.
"""

from __future__ import annotations

import os
from pathlib import Path

_ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"


def _load_env_file(path: Path) -> None:
    """Load ``KEY=VALUE`` lines from *path* into the environment.

    Existing environment variables take precedence. Values may be wrapped in
    single or double quotes, which are stripped.
    """

    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip().strip("\"'")


_load_env_file(_ENV_PATH)


def env(key: str, default: str | None = None) -> str:
    """Return the value of ``key`` or *default* when provided.

    Raises ``RuntimeError`` when the variable is required but not defined.
    """

    value = os.environ.get(key)
    if value is None:
        if default is None:
            raise RuntimeError(f"Missing required environment variable: {key}")
        return default
    return value


def env_bool(key: str, default: bool = False) -> bool:
    """Return the boolean interpretation of ``key``."""

    value = os.environ.get(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(key: str, default: str = "") -> list[str]:
    """Return the comma-separated list value of ``key``."""

    value = os.environ.get(key, default)
    return [item.strip() for item in value.split(",") if item.strip()]
