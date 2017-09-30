from django.forms import CharField

from .widgets import SplitInputWidget


class SplitCharField(CharField):
    widget = SplitInputWidget
    splitter = ''

    def __init__(self, *args, **kwargs):
        """Construct."""
        super().__init__(*args, **kwargs)
        if 'splitter' in kwargs:
            self.splitter = kwargs['splitter']

    def clean(self, value):
        """Clean the field and replace None values with an empty string."""
        return self.splitter.join([item if item is not None else '' for item in value])