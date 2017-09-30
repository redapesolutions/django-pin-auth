from django.test import TestCase
from faker import Faker
import mock
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.conf import settings
from django.core.urlresolvers import reverse

from django_pin_auth.models import SingleUseToken

fake = Faker('ru_RU')  # anything that's UTF8 will do


def make_pins(token):
    pins = {}
    for i, character in enumerate(token):
        pins['pin_%s' % i] = character
    return pins


class TestVerification(TestCase):
    """Test the verification"""
    def setUp(self):
        self.user = User.objects.create_user(username=fake.email())
        self.token1 = SingleUseToken.objects.create(user=self.user)
        self.token2 = SingleUseToken.objects.create(user=self.user)
        self.url = reverse('django_pin_auth:enter_pin')

    def attempt_to_authenticate(self, user, token):
        pins = make_pins(token.token)
        return self.client.post(self.url, data={
            'email': user.username if user else fake.email(),
            **pins
        })

    def test_fails_when_wrong_token(self):
        """Should redirect and not end up with authenticated user."""
        response = self.attempt_to_authenticate(None, self.token1)
        assert response.status_code == 200
        user = get_user(self.client)
        assert user.is_authenticated() is False
        assert response.request['PATH_INFO'] == self.url

    def test_success_with_valid(self):
        """Should have the correct user and redirect."""
        response = self.attempt_to_authenticate(self.user, self.token1)
        user = get_user(self.client)
        assert user.is_authenticated()
        assert user == self.user
        assert response.url == '/hello'  # redirected to settings' login redirect url
