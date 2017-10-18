# -*- coding: utf-8
from django.apps import AppConfig
from datetime import timedelta
from .read_policies import ReadPolicy
from django.conf import settings

class DjangoPinAuthConfig(AppConfig):
    name = 'django_pin_auth'
    pin_validity = timedelta(minutes=5)
    read_policy = ReadPolicy.delete
    username_field = getattr(settings, 'USERNAME_FIELD', 'username')
