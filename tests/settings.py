# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import os
import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "11111111111111111111111111111111111111111111111111"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django_pin_auth.apps.DjangoPinAuthConfig",
]

TIME_ZONE = 'America/Chicago'

SITE_ID = 1


MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'tests', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGIN_URL = 'pinauth/enterpin'
LOGIN_REDIRECT_URL = '/hello'

AUTHENTICATION_BACKENDS = [
    'django_pin_auth.auth_backend.PinBackend',
]