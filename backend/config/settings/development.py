"""Development environment settings."""

from config.env import env_list

from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1,[::1]")
