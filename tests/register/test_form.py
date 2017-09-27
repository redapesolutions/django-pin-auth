from django.test import TestCase
from faker import Faker
from django.contrib.auth.models import User


from django_pin_auth import forms

fake = Faker('ru_RU')  # anything that's UTF8 will do

class TestForm(TestCase):
    """Test the form"""
    def setUp(self):
        self.user = User.objects.create_user(username=fake.email())

    def test_unique_email(self):
        """Should not allow an email that is already attached to a user."""
        form = forms.RegisterForm({
            'email': self.user.username
        })
        assert form.is_valid() is False
        assert 'login' in form.errors['email'][0]

    def test_ok_email(self):
        """Works with email."""
        form = forms.RegisterForm({
            'email': fake.email()
        })
        assert form.is_valid() is True