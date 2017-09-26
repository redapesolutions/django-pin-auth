#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-pin-auth
------------

Tests for `django-pin-auth` models module.
"""

from django.test import TestCase
from django.apps import apps

from django_pin_auth import models
from django_pin_auth.read_policies import ReadPolicy


class TestCreateDelete(TestCase):

    def setUp(self):
        self.token = models.SingleUseToken.objects.create()

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

    def tearDown(self):
        pass
