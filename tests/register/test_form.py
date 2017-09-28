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


class TestFormUserCreate(TestCase):
    def test_user_should_be_created(self):
        """With correct email."""
        email = fake.email()
        form = forms.RegisterForm({
            'email': email
        })
        # Need to use is_valid to get cleaned data
        form.is_valid()
        form.save()
        assert form.user.username == email
        assert form.user.password != ''


class TestFormTokenCreate(TestCase):
    def test_token_should_be_created(self):
        """With correct user."""
        email = fake.email()
        form = forms.RegisterForm({
            'email': email
        })
        # Need to use is_valid to get cleaned data
        form.is_valid()
        form.save()
        assert form.token.user == form.user
        assert form.token.is_valid()


class TestSendEmail(TestCase):
    """Test the sending of email"""
    def setUp(self):
        self.email = fake.email()
        self.form = forms.RegisterForm({
            'email': self.email
        })
        self.form.is_valid()
        self.form.save()
        self.request = RequestFactory().get('/')

    def test_sender_set_correctly(self):
        """Should use _get_email_sender to get the sender."""
        email = fake.email()
        self.form._get_email_sender = mock.MagicMock(return_value=email)
        self.form.send_email(self.request)
        email_sent = mail.outbox[0]
        assert email_sent.from_email == email

    def test_recipient(self):
        """Should use the user's email to get the sender."""
        email = fake.email()
        self.form._get_email_sender = mock.MagicMock(return_value=email)
        self.form.send_email(self.request)
        email_sent = mail.outbox[0]
        assert email_sent.to.__len__() == 1
        assert email_sent.to[0] == self.email
