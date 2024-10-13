import os
from datetime import timedelta, date
from pathlib import Path
from collections import OrderedDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")


# Application definition

APPLICATION_NAME = "TechGiants"

CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    "constance",
]

INTERNAL_APPS = [
    "applications.members",
    "applications.jwtauth",
]

INSTALLED_APPS = CORE_APPS + THIRD_PARTY_APPS + INTERNAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "system.urls"
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "constance.context_processors.config",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]

WSGI_APPLICATION = "system.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["DATABASE_NAME"],
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PASSWORD"],
        "HOST": os.environ["DATABASE_HOST"],
        "PORT": os.environ["DATABASE_PORT"],
    }
}

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

LANGUAGE_CODE = "ru-RU"
USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "members.User"

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "applications.common.exception_handler.custom_exception_handler",
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "applications.members.permissions.IsFilledProfile",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "applications.jwtauth.authentication.CustomAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}
APPEND_SLASH = False
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=14),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_COOKIE": "token",
}

SPECTACULAR_SETTINGS = {
    "TITLE": f"{APPLICATION_NAME} API",
    "DESCRIPTION": "",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_PREFLIGHT_MAX_AGE = 7200
CORS_ORIGIN_WHITELIST = os.getenv("CORS_ORIGIN_WHITELIST", "").split(",")
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-timezone",
    "cache-control",
    "pragma",
    "expires",
    "skip-error-interceptor",
]
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

ACTIVE_CONFERENCE = OrderedDict(
    [
        ("GRADE", ("Всероссийская", "Уровень конференции")),
        ("SHORT_NAME", ("Конференция по ИБ", "Короткое название конференции")),
        ("START_DATE", (date(2022, 11, 1), "Дата начала конференции", date)),
        ("DURATION", ("2 часа", "Продолжительность конференции")),
        ("FORMAT", ("Онлайн", "Формат конференции")),
        (
            "NAME",
            (
                "Международная научно-практическая конференция «Информационная безопасность»",
                "Название конференции",
            ),
        ),
    ]
)
ACTIVE_CONFERENCE_CONSTANCE_PREFIX = "CONFERENCE_"

CONSTANCE_CONFIG = OrderedDict(
    [
        *[
            (f"{ACTIVE_CONFERENCE_CONSTANCE_PREFIX}{k}", v)
            for k, v in ACTIVE_CONFERENCE.items()
        ]
    ]
)

CONSTANCE_CONFIG_FIELDSETS = OrderedDict(
    [
        (
            "Активная конференция",
            [
                f"{ACTIVE_CONFERENCE_CONSTANCE_PREFIX}{k}"
                for k in ACTIVE_CONFERENCE.keys()
            ],
        ),
    ]
)

MEDIA_ROOT = BASE_DIR / "uploads"
MEDIA_URL = "/uploads/"
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST
