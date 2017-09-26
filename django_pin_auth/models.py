# -*- coding: utf-8 -*-
import random
import datetime

from django.db import models
from django.apps import apps

from model_utils.models import (
    TimeStampedModel,
    SoftDeletableModel
)

from .read_policies import ReadPolicy

config = apps.get_app_config('django_pin_auth')


class SingleUseToken(TimeStampedModel, SoftDeletableModel):
    """Single use token model. """
    token = models.CharField(max_length=255)

    all_objects = models.Manager()

    def make_token(self):
        return random.randint(100000, 999999)

    def save(self, *args, **kwargs):
        """Save model. Create value for token."""
        if self._state.adding:
            self.token = str(self.make_token())
        super().save(*args, **kwargs)

    def is_valid(self):
        """Get the validity of the token.
        
        Looks at the time since creation and compares that with config value if any
        """
        # No validity set
        if config.pin_validity is None:
            return True

        # Validity check
        # TimeStampedModel sets a timezone aware dt, thankfully not depending on settings, but UTC
        return datetime.datetime.now(datetime.timezone.utc) < self.created + config.pin_validity

    def read(self):
        """Read the token.
        
        Depending on config, get rid of it entirely or just mark it as read
        """
        if config.read_policy is ReadPolicy.mark:
            self.delete()
        elif config.read_policy is ReadPolicy.delete:
            # Go harder and actually delete via normal manager
            self.__class__.all_objects.filter(pk=self.pk).delete()

    def __str__(self):
        return 'Singe use token %s' % self.token
    


