# -*- coding: utf-8 -*-

from django.db import models

from model_utils.models import (
    TimeStampedModel,
    SoftDeletableModel
)


class SingleUseToken(TimeStampedModel, SoftDeletableModel):
    """Single use token model. """
    def is_valid(self):
        """Get the validity of the token.
        
        Looks at the time since creation and compares that with config value if any

        TODO
        """
        pass

    def read(self):
        """Read the token.
        
        Depending on config, get rid of it entirely or just mark it as read

        TODO
        """
        pass
    


