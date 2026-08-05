"""Shared Django settings for every environment.

Governing documents: SPEC-001, ARCH-001, ADR-002, ADR-003, OPS-001.
Environment-specific and sensitive values are read from the environment; no
secrets are hardcoded in this module.
"""

from pathlib import Path

from config.env import env, env_bool, env_list

# --- Paths ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPO_ROOT = BASE_DIR.parent
FRONTEND_DIR = REPO_ROOT / "frontend"

# --- Core configuration -------------------------------------------------------

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env_bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", default="")

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Applications -------------------------------------------------------------
# Product modules are limited to those approved by SPEC-001. Authentication and
# administrative components are outside Release 1 scope per ARCH-001 (17.9).

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "apps.core.apps.CoreConfig",
    "apps.home.apps.HomeConfig",
    "apps.about.apps.AboutConfig",
    "apps.skills.apps.SkillsConfig",
    "apps.experience.apps.ExperienceConfig",
    "apps.portfolio.apps.PortfolioConfig",
    "apps.common.apps.CommonConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- Templates ----------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [FRONTEND_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

# --- Database -----------------------------------------------------------------
# Connection only; schema is created by approved migrations.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="postgres"),
        "USER": env("POSTGRES_USER", default="postgres"),
        "PASSWORD": env("POSTGRES_PASSWORD", default=""),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

# --- Static, media and locale -------------------------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [FRONTEND_DIR / "static"]
STATIC_ROOT = REPO_ROOT / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = REPO_ROOT / "media"

LOCALE_PATHS = [BASE_DIR / "locale"]

# --- Internationalization -----------------------------------------------------

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("pt-br", "Portuguese (Brazil)"),
]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Logging ------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
