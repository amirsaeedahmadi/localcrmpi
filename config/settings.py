"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import logging
import logging.config
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-w^eca+^l*2j15t%t5v*oyfg26yl$ppa16)cs&te)yk8)g6+4ii",
)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
ADMIN_ALLOWED_HOSTS = env.list("DJANGO_ADMIN_ALLOWED_HOSTS", default=[])

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
    "django_extensions",
    "drf_yasg",
    "rest_framework_simplejwt",
    "crm",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

MEDIA_ROOT = "media"
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/crm/media/"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
logging.config.dictConfig(LOGGING)

# Kafka
KAFKA_URL = env.list("KAFKA_URL")

# CRM
CRM_SETTINGS = {
    "CRM_BASE_API_URL": env.str("CRM_BASE_API_URL"),
    "CRM_ADMIN_USERNAME": env.str("CRM_ADMIN_USERNAME"),
    "CRM_ADMIN_PASSWORD": env.str("CRM_ADMIN_PASSWORD"),
}

CRM_PANEL_USER_ID_FIELD = env.str("CRM_PANEL_USER_ID_FIELD", default="cf_1221")
CRM_PANEL_COMPANY_ID_FIELD = env.str("CRM_PANEL_COMPANY_ID_FIELD", default="cf_1223")
CRM_PANEL_PERFORMA_ID_FIELD = env.str("CRM_PANEL_PERFORMA_ID_FIELD", default="cf_1225")
CRM_PANEL_SERVICE_REQUEST_ID_FIELD = env.str(
    "CRM_PANEL_SERVICE_REQUEST_ID_FIELD", default="cf_1227"
)
CRM_PERSONNEL_ID_FIELD = env.str("CRM_PERSONNEL_ID_FIELD", default="panelid")
CRM_PANEL_PERFORMA_REF_CODE_FIELD = env.str(
    "CRM_PANEL_PERFORMA_REF_CODE_FIELD", default="quote_no"
)
CRM_PANEL_PERFORMA_DURATION_FIELD = env.str(
    "CRM_PANEL_PERFORMA_DURATION_FIELD", default="cf_1126"
)
DEFAULT_QUOTE_TEMPLATE_ID = env.str("DEFAULT_QUOTE_TEMPLATE_ID", default=10)
