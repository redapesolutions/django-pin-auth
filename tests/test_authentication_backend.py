import mock
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from faker import Faker

from django_pin_auth.models import SingleUseToken
from django_pin_auth.auth_backend import PinBackend

fake = Faker('hu_HU')  # anything that's UTF8 will do

class TestAuth(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username=fake.email())
        self.user2 = User.objects.create_user(username=fake.email())
        self.token1a = SingleUseToken.objects.create(user=self.user1)
        self.token1b = SingleUseToken.objects.create(user=self.user1)
        # Make that second one invalid
        self.token1b.is_valid = mock.MagicMock(return_value=False)
        self.backend = PinBackend()
        self.request = RequestFactory().get('/')

    def test_no_user(self):
        """None when no corresponding user."""
        assert self.backend.authenticate(self.request, email=fake.email(), pin=self.token1a.token) is None
    
    def test_no_token(self):
        """None when no token is provided."""
        assert self.backend.authenticate(self.request, email=self.user1.username, pin=None) is None

    def test_user_wrong_pin(self):
        """None when token is wrong user."""
        assert self.backend.authenticate(self.request, email=self.user2.username, pin=self.token1a.token) is None
    
    def test_user_invalid_pin(self):
        """None when pin isn't valid anymore."""
        # Mock the _get_token method on backend so it returns our token1b with mocked is_valid
        self.backend._get_token = mock.MagicMock(return_value=self.token1b)
        assert self.backend.authenticate(self.request, email=self.user1.username, pin=self.token1b.token) is None
    
    def test_user_pin_twice(self):
        """Can't reuse pin."""
        self.backend.authenticate(self.request, email=self.user1.username, pin=self.token1a.token)
        assert self.backend.authenticate(self.request, email=self.user1.username, pin=self.token1a.token) is None

    def test_user_all_good(self):
        """Returns the user."""
        assert self.backend.authenticate(self.request, email=self.user1.username, pin=self.token1a.token) == self.user1
    