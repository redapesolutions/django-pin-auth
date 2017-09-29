from django.forms import CharField

from .widgets import SplitInputWidget


class SplitCharField(CharField):
    widget = SplitInputWidget
    splitter = ''

    def __init__(self, *args, **kwargs):
        if 'splitter' in kwargs:
            self.splitter = kwargs['splitter']

        super().__init__(*args, **kwargs)

    def clean(self, value):
        return self.splitter.join(value)