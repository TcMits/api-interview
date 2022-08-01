from datetime import timedelta
import os
import socket  # only if you haven't already imported this
import warnings
import ast

import dj_database_url
import django_cache_url
from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _

__, __, ips = socket.gethostbyname_ex(socket.gethostname())

INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + [
    "127.0.0.1",
    "10.0.2.2",
    "0.0.0.0",
    "localhost",
]

AUTH_USER_MODEL = "account.User"


def get_list(text):
    return [item.strip() for item in text.split(",")]


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e
    return default_value


DEBUG = get_bool_from_env("DEBUG", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY and DEBUG:
    warnings.warn("SECRET_KEY not configured, using a random temporary key.")
    SECRET_KEY = get_random_secret_key()

ALLOWED_HOSTS = get_list(
    os.environ.get("ALLOWED_HOSTS", ",".join(INTERNAL_IPS) + ",localhost")
)


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "src.account.apps.AccountConfig",
    "rest_framework",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "src.core.middlewares.AuthenticationMiddleware",
]

ROOT_URLCONF = "src.urls"
BASE_URL = "https://example.com"

AUTHENTICATION_BACKENDS = [
    "src.core.auth_backends.ModelBackend",
    "src.core.auth_backends.JSONWebTokenBackend",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "src.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DB_MAX_CONNECTION = 100
CONN_MAX_AGE = 0
STATEMENT_TIMEOUT = 90000

DATABASES = {
    "default": {
        **dj_database_url.config(
            conn_max_age=CONN_MAX_AGE,
            default=f"sqlite:////{os.path.join(PROJECT_ROOT,'db.sqlite3')}",
        ),
    }
}

# from rest_framework.parsers import MultiPartParser, FormParser
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "src.core.api_authentication.APIAuthentication",
    ],
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

TIME_ZONE = "Asia/Saigon"

LANGUAGE_CODE = "vi"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ("vi", _("Vietnamese")),
]

LOCALE_PATHS = [os.path.join(PROJECT_ROOT, "locale")]


# Some cloud providers (Heroku) export REDIS_URL variable instead of CACHE_URL
REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    CACHE_URL = os.environ.setdefault("CACHE_URL", REDIS_URL)
    CACHEOPS_REDIS = os.environ.setdefault("CACHEOPS_REDIS", REDIS_URL)

CACHES = {"default": django_cache_url.config()}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
DEFAULT_FILE_STORAGE = os.environ.get(
    "DEFAULT_FILE_STORAGE", "django.core.files.storage.FileSystemStorage"
)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
MEDIA_URL = "/store/media/"

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATIC_URL = "/store/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["default"]},
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "verbose": {
            "format": (
                "%(levelname)s %(name)s %(message)s [PID:%(process)d:%(threadName)s]"
            )
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "json",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server" if DEBUG else "json",
        },
        "celery_app": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "celery_json",
        },
        "celery_task": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "celery_task_json",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django": {"level": "INFO", "propagate": True},
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "celery.app.trace": {
            "handlers": ["celery_app"],
            "level": "INFO",
            "propagate": False,
        },
        "celery.task": {
            "handlers": ["celery_task"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

JWT_TTL_ACCESS = timedelta(seconds=3600 * 24)
JWT_TTL_REFRESH = timedelta(seconds=3600 * 24 * 7)
