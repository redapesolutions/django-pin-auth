from django import forms
from django.db import models


class SplitInputWidget(forms.widgets.MultiWidget):

    def __init__(self, count=6, input_type='text', *args, **kwargs):
        widgets = (
            forms.TextInput(attrs={'size': 1, 'type': input_type}),
        ) * count
        self.count = count
        super().__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        empty = [''] * self.count
        if value:
            padded = (value.split('') + empty)[:self.count]
            return padded
        return empty
