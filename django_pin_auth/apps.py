# -*- coding: utf-8
from django.apps import AppConfig
from datetime import timedelta
from enum import Enum

READ_POLICY = Enum(
    delete=1
    mark=2
)

class DjangoPinAuthConfig(AppConfig):
    name = 'django_pin_auth'
    pin_validity = timedelta(minutes=5)
    read_policy = READ_POLICY.delete
