# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.views.generic import (
    TemplateView
)
from django.shortcuts import redirect

from .models import (
	SingleUseToken,
)

from .forms import RegisterForm


class RegisterView(FormView):
    """Register view."""
    template_name = 'django_pin_auth/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        """Handle valid form."""
        form.send_email(self.request)
        return redirect('django_pin_auth:enter_pin')


# TODO
class EnterPinView(FormView):
    """Page where users enter their pin."""
    template_name = 'django_pin_auth/register.html'
    form_class = RegisterForm
