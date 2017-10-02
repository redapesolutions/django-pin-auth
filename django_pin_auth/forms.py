from django.apps import apps
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from .models import SingleUseToken
from .fields import SplitCharField

def _get_user_model(email):
    user_model = get_user_model()
    return (user_model, {
        user_model.USERNAME_FIELD: email
    })

class LoginForm(forms.Form):
    email = forms.EmailField(label='Please provide a valid email')
    body_template = 'django_pin_auth/emails/login_body.html'
    subject_template = 'django_pin_auth/emails/login_subject.txt'

    def get_register_body_template(self):
        return self.body_template

    def get_register_subject_template(self):
        return self.subject_template

    def get_user(self, user_model, **kwargs):
        return user_model.objects.get(**kwargs)

    def create_token(self, user):
        return SingleUseToken.objects.create(user=user)

    def prepare_form(self):
        email = self.cleaned_data['email']
        user_model, kwargs = _get_user_model(email)
        self.user = self.get_user(user_model, **kwargs)
        self.token = self.create_token(self.user)

    def clean_email(self):
        """Clean the email data.

        Checks that email exists in db
        """
        email = self.cleaned_data.get('email')
        user_model, filter_kw = _get_user_model(email)
        if not user_model.objects.filter(**filter_kw).exists():
            raise forms.ValidationError('Invalid user')
        return email

    def send_email(self, request):
        """Send pin email."""
        self.prepare_form()
        context = self._build_context(request, token=self.token, valid_until=self.token.valid_until_timestamp(), pin=self.token.token)
        html = render_to_string(
            self.get_register_body_template(),
            context
        )
        subject = render_to_string(
            self.get_register_subject_template(),
            context
        )
        sender = self._get_email_sender(request)
        email = self.cleaned_data['email']
        msg = EmailMessage(subject=subject, body=html, from_email=sender, to=[email])
        msg.content_subtype = "html"
        return msg.send()

    def _build_context(self, request, **kwargs):
        """Build the context for emails."""
        site = get_current_site(request)
        return dict(**{
            'current_site': site
        }, **self.cleaned_data, **kwargs)

    def _get_email_sender(self, request):
        """Get email address to send from."""
        config = apps.get_app_config('django_pin_auth')
        return getattr(config, 'email_sender', getattr(settings, 'DEFAULT_FROM_EMAIL'))


class RegisterForm(LoginForm):
    body_template = 'django_pin_auth/emails/register_body.html'
    subject_template = 'django_pin_auth/emails/register_subject.txt'

    def _build_login_vs_register_message(self):
        """Helper to build a "friendly" message"""
        link_to_login = '<a href="%s">login</a>' % reverse('django_pin_auth:register')
        return mark_safe(
            'That email address already exists. Did you mean to %s?' % link_to_login
        )

    def clean_email(self):
        """Clean the email data.

        Checks for unicity
        """
        email = self.cleaned_data.get('email')
        user_model, filter_kw = _get_user_model(email)
        if user_model.objects.filter(**filter_kw).exists():
            raise forms.ValidationError(self._build_login_vs_register_message())
        return email

    def get_user(self, user_model, **kwargs):
        """Create user."""
        user = user_model.objects.create(**kwargs)
        user.set_unusable_password()
        return user


class PinForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    pin = SplitCharField()

    def clean(self):
        """Perform last validation by checking that user can authenticate."""
        self.user = authenticate(self.request, **self.cleaned_data)

        if self.user is None:
            raise forms.ValidationError('Invalid credentials')
