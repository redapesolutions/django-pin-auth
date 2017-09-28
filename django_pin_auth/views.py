# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.views.generic import (
    TemplateView
)
from django.shortcuts import redirect

from .models import (
	SingleUseToken,
)

from .forms import RegisterForm, PinForm


class RegisterView(FormView):
    """Register view."""
    template_name = 'django_pin_auth/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        """Handle valid form."""
        self.request.session['email'] = form.cleaned_data['email']
        form.save()
        form.send_email(self.request)
        return redirect('django_pin_auth:enter_pin')


class EnterPinView(FormView):
    """Page where users enter their pin."""
    template_name = 'django_pin_auth/enter_pin.html'
    form_class = PinForm
    
    def get_context_data(self):
        """Get context for pin verification view."""
        context = super().get_context_data()
        context['email'] = self.request.session.get('email')
        return context
