# -*- coding: utf-8 -*-
from django.views.generic.edit import FormView
from django.views.generic import (
    TemplateView
)
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.conf import settings

from .models import (
	SingleUseToken,
)

from .forms import RegisterForm, PinForm


class RegisterView(FormView):
    """Register view."""
    template_name = 'django_pin_auth/register.html'
    form_class = RegisterForm

    def dispatch(self, request):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
    
        return super().dispatch(request)

    def form_valid(self, form):
        """Handle valid form."""
        self.request.session['email'] = form.cleaned_data['email']
        form.save()
        form.send_email(self.request)
        return redirect('django_pin_auth:register_pin')


class EnterPinView(FormView):
    """Page where users enter their pin."""
    template_name = 'django_pin_auth/enter_pin.html'
    form_class = PinForm

    def get_initial(self):
        return {
            'email': self.request.session.get('email')
        }
    
    def get_context_data(self, form=None):
        """Get context for pin verification view."""
        context = super().get_context_data()
        context['email'] = self.request.session.get('email')
        return context

    def successful_login_url(self):
        return self.request.POST.get('next', settings.LOGIN_REDIRECT_URL)

    def failed_login_url(self):
        return settings.LOGIN_URL

    def form_valid(self, form):
        """Handle valid form."""
        email = form.cleaned_data['email']
        pin = form.cleaned_data['pin']
        
        user = authenticate(self.request, email=email, pin=pin)

        if user is None:
            # TODO assume that the django contrib message is being used?
            where_to_next = self.failed_login_url()
        else:
            # TODO Should we force to use the Pin backend?
            login(self.request, user)
            where_to_next = self.successful_login_url()

        return redirect(where_to_next)

class RegistrationEnterPinView(EnterPinView):
    def failed_login_url(self):
        return 'django_pin_auth:register_pin'
