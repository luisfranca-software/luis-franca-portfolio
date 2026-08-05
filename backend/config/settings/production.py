"""Production environment settings."""

from config.env import env_list

from .base import *  # noqa: F401, F403

DEBUG = False
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")

# Transport security per ARCH-001 (17.5): HTTPS is mandatory in production.
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
