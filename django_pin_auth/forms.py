from django.apps import apps
from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from .models import SingleUseToken
from .fields import SplitCharField

class RegisterForm(forms.Form):
    email = forms.EmailField(label='Please provide a valid email')
    register_body_template = 'django_pin_auth/emails/register_body.html'
    register_body_subject = 'django_pin_auth/emails/register_subject.txt'

    def get_register_body_template(self):
        return self.register_body_template

    def get_register_body_subject(self):
        return self.register_body_subject

    def send_email(self, request):
        """Send registration email."""
        email = self.cleaned_data['email']
        context = self._build_context(request, pin=self.token.token)
        html = render_to_string(
            self.get_register_body_template(),
            context
        )
        subject = render_to_string(
            self.get_register_body_subject(),
            context
        )
        sender = self._get_email_sender(request)
        msg = EmailMessage(subject=subject, body=html, from_email=sender, to=[email])
        msg.content_subtype = "html"
        return msg.send()

    def _build_context(self, request, **kwargs):
        """Build the context for emails."""
        site = get_current_site(request)
        return dict(**{
            'current_site': site
        }, **self.cleaned_data, **kwargs)

    def _build_login_vs_register_message(self):
        """Helper to build a "friendly" message"""
        link_to_login = '<a href="%s">login</a>' % reverse('django_pin_auth:register')
        return mark_safe(
            'That email address already exists. Did you mean to %s?' % link_to_login
        )

    def _get_email_sender(self, request):
        """Get email address to send from."""
        config = apps.get_app_config('django_pin_auth')
        return getattr(config, 'email_sender', getattr(settings, 'DEFAULT_FROM_EMAIL'))

    def clean_email(self):
        """Clean the email data.

        Checks for unicity as well
        """
        email = self.cleaned_data.get('email')
        user_model = get_user_model()
        filter_kw = {
            user_model.USERNAME_FIELD: email
        }
        if user_model.objects.filter(**filter_kw).exists():
            raise forms.ValidationError(self._build_login_vs_register_message())
        return email

    def create_user(self, email):
        user_model = get_user_model()
        kwargs = {
            user_model.USERNAME_FIELD: email
        }
        user = user_model.objects.create(**kwargs)
        user.set_unusable_password()
        return user

    def create_token(self, user):
        return SingleUseToken.objects.create(user=user)

    def save(self):
        """Create user and token."""
        self.user = self.create_user(self.cleaned_data['email'])
        self.token = self.create_token(self.user)


class PinForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    pin = SplitCharField()
