"""Shared Django settings for every environment.

Governing documents: SPEC-001, SPEC-002, ARCH-001, ADR-002, ADR-003, ADR-004,
OPS-001.
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
# Product modules are limited to those approved by SPEC-001. Release 2 adds
# Django's native administration and authentication components per ARCH-001
# (17.9) and ADR-001 (Release 2 — Platform Evolution).

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "apps.core.apps.CoreConfig",
    "apps.home.apps.HomeConfig",
    "apps.about.apps.AboutConfig",
    "apps.skills.apps.SkillsConfig",
    "apps.experience.apps.ExperienceConfig",
    "apps.portfolio.apps.PortfolioConfig",
    "apps.common.apps.CommonConfig",
    "apps.contact.apps.ContactConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.common.middleware.AnalyticsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
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
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "apps.common.context_processors.public_contact_links",
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

# --- Email / transactional notifications ---------------------------------------
# Provider and isolation decisions: ADR-004 (Brevo SMTP). All values originate
# from the environment; credentials are never hardcoded.

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env("EMAIL_PORT", default="587")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="")

# --- Contact module -------------------------------------------------------------
# Governing documents: SPEC-002 (sections 7, 8), ARCH-001 (15.7, 16.3), ADR-004.

CONTACT_NOTIFICATION_EMAIL = env("CONTACT_NOTIFICATION_EMAIL", default="")
CONTACT_RETENTION_DAYS = int(env("CONTACT_RETENTION_DAYS", default="90"))

# --- Analytics (Release 1.1) --------------------------------------------------
# Essential analytics with data minimization. Server-side events are stored in
# PostgreSQL; no third-party provider or PII is collected. Disabled by setting
# ANALYTICS_ENABLED=False in the environment.

ANALYTICS_ENABLED = env_bool("ANALYTICS_ENABLED", default=True)
ANALYTICS_RETENTION_DAYS = int(env("ANALYTICS_RETENTION_DAYS", default="365"))

# Public professional links are presentation configuration per ARCH-001 (16.3);
# values differ per environment and are never secrets.
CONTACT_LINKS = {
    "whatsapp": env("WHATSAPP_CONTACT_URL", default=""),
    "linkedin": env("LINKEDIN_PROFILE_URL", default=""),
    "github": env("GITHUB_PROFILE_URL", default=""),
    "resume": env("RESUME_URL", default=""),
}

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
