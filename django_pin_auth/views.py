# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.views.generic import (
    TemplateView
)
from django.contrib.auth import login
from django.shortcuts import redirect
from django.conf import settings

from .models import (
	SingleUseToken,
)

from .forms import LoginForm, RegisterForm, PinForm


class LoginView(FormView):
    """Login view."""
    template_name = 'django_pin_auth/login.html'
    form_class = LoginForm

    def dispatch(self, request):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
    
        return super().dispatch(request)

    def form_valid(self, form):
        """Handle valid form."""
        self.request.session['email'] = form.cleaned_data['email']
        form.send_email(self.request)
        return redirect('django_pin_auth:enter_pin')


class RegisterView(LoginView):
    """Register view."""
    template_name = 'django_pin_auth/register.html'    
    form_class = RegisterForm


class EnterPinView(FormView):
    """Page where users enter their pin."""
    template_name = 'django_pin_auth/enter_pin.html'
    form_class = PinForm

    def get_initial(self):
        """Initial state of the form."""
        return {
            'email': self.request.session.get('email')
        }
    
    def get_context_data(self, form=None):
        """Get context for pin verification view."""
        context = super().get_context_data()
        context['email'] = self.request.session.get('email')
        return context

    def get_form(self):
        form = super().get_form()
        form.request = self.request
        return form

    def form_valid(self, form):
        """Handle valid form."""
        login(self.request, form.user)
        
        return redirect(
            self.request.POST.get('next', settings.LOGIN_REDIRECT_URL)
        )
