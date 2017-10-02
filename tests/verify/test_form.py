from django.test import TestCase, RequestFactory
from faker import Faker
from django.contrib.auth.models import User
import mock
from django.core import mail

from django_pin_auth import forms

fake = Faker('ru_RU')  # anything that's UTF8 will do

class TestForm(TestCase):
    """Test the form"""
    def setUp(self):
        self.user = User.objects.create_user(username=fake.email())

    def test_existing_email(self):
        """Should block if email doesn't exist."""
        form = forms.LoginForm({
            'email': fake.email()
        })
        assert form.is_valid() is False

    def test_ok_email(self):
        """Works with email."""
        form = forms.LoginForm({
            'email': self.user.username
        })
        assert form.is_valid() is True
