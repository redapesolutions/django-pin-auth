from django import forms
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

class RegisterForm(forms.Form):
    email = forms.EmailField(label='Please provide a valid email')

    def send_email(self, request):
        email = self.cleaned_data['email']
        context = self._build_context(request, pin='1223')
        html = render_to_string(
            'django_pin_auth/emails/register_body.html',
            context
        )
        subject = render_to_string(
            'django_pin_auth/emails/register_subject.txt',
            context
        )
        sender = 'a@a.com'  # TODO
        msg = EmailMessage(subject=subject, body=html, from_email=sender, to=[email])
        msg.content_subtype = "html"
        return msg.send()

    def _build_context(self, request, **kwargs):
        site = get_current_site(request)
        return dict(**{
            'current_site': site
        }, **self.cleaned_data, **kwargs)

    def _build_login_vs_register_message(self):
        link_to_login = '<a href="%s">login</a>' % reverse('django_pin_auth:register')
        return mark_safe(
            'That email address already exists. Did you mean to %s?' % link_to_login
        )

    def clean_email(self):
        """Clean the email data.

        Checks for unicity as well
        """
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(username=email).exists():
            raise forms.ValidationError(self._build_login_vs_register_message())
        return email