# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        regex=r"register/?$",
        view=views.RegisterView.as_view(),
        name='register',
    ),
    url(
        regex=r"enterpin/?$",
        view=views.EnterPinView.as_view(),
        name='enter_pin',
    ),
    url(
        regex=r"welcome/?$",
        view=views.RegistrationEnterPinView.as_view(),
        name='register_pin',
    ),
]
