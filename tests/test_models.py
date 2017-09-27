#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-pin-auth
------------

Tests for `django-pin-auth` models module.
"""
import mock
import datetime

from django.test import TestCase
from django.apps import apps
from django.contrib.auth.models import User
from faker import Faker

from django_pin_auth import models
from django_pin_auth.read_policies import ReadPolicy

fake = Faker('ja_JP')  # anything that's UTF8 will do

class TokenCreate(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=fake.email())
        self.token = models.SingleUseToken.objects.create(user=self.user)

class TestCreateDelete(TokenCreate):
    def test_create_token_value(self):
        """Should automatically create a 6 digit token."""
        assert self.token.token.__len__() == 6
        for character in self.token.token:
            try:
                int(character)
            except ValueError:
                raise AssertionError('Character "%s" is not a digit' % character)

    def test_read_gone(self):
        """After read, shouldn't be found by the manager, regardless of policy."""
        self.token.read()
        with self.assertRaises(models.SingleUseToken.DoesNotExist):
            models.SingleUseToken.objects.get(pk=self.token.pk)

    def test_read_full_delete(self):
        """After read, should be totally gone if policy is delete (default)."""
        self.token.read()
        with self.assertRaises(models.SingleUseToken.DoesNotExist):
            models.SingleUseToken.all_objects.get(pk=self.token.pk)

    def test_read_soft_delete(self):
        """After read, should be still there, just disabled, if policy is mark."""
        config = apps.get_app_config('django_pin_auth')
        config.read_policy = ReadPolicy.mark
        self.token.read()
        try:
            models.SingleUseToken.all_objects.get(pk=self.token.pk)
        except models.SingleUseToken.DoesNotExist:
            raise AssertionError('Token should still exist')
        config.read_policy = ReadPolicy.delete


class TestValidity(TokenCreate):
    @mock.patch('django_pin_auth.models.datetime')
    def test_valid_within_timerange(self, mock_dt):
        """Token is valid within the time provided."""
        config = apps.get_app_config('django_pin_auth')
        mock_dt.datetime.now = mock.Mock(return_value=datetime.datetime.now(datetime.timezone.utc)+config.pin_validity-datetime.timedelta(seconds=1))
        assert self.token.is_valid() is True

    @mock.patch('django_pin_auth.models.datetime')
    def test_invalid_after_timerange(self, mock_dt):
        """Token is invalid after the time provided."""
        config = apps.get_app_config('django_pin_auth')
        mock_dt.datetime.now = mock.Mock(return_value=datetime.datetime.now(datetime.timezone.utc)+config.pin_validity+datetime.timedelta(seconds=1))
        assert self.token.is_valid() is False
    
    @mock.patch('django_pin_auth.models.datetime')
    def test_always_valid(self, mock_dt):
        """Token is always valid if no time given."""
        config = apps.get_app_config('django_pin_auth')
        keep_value = config.pin_validity
        config.pin_validity = None
        mock_dt.datetime.now = mock.Mock(return_value=datetime.datetime(2713, 12, 25))
        assert self.token.is_valid() is True
        config.pin_validity = keep_value

class TestUserToken(TokenCreate):
    def setUp(self):
        super().setUp()
        # Copy the values and do it again
        self.user2 = self.user
        self.token2 = self.token
        super().setUp()

    def test_correct_user_token(self):
        """Should find token."""
        self.assertEqual(models.get_user_token(self.user, self.token.token), self.token)

    def test_incorrect_user(self):
        """Should not find token with not correct user."""
        self.assertEqual(models.get_user_token(self.user2, self.token), None)
    
    def test_incorrect_token(self):
        """Should not find token with not correct token.
        
        Well, which is incorrect is relative..."""
        self.assertEqual(models.get_user_token(self.user2, self.token), None)