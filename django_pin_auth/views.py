# -*- coding: utf-8 -*-
from django.views.generic import (
    TemplateView
)

from .models import (
	SingleUseToken,
)


class RegisterView(TemplateView):
    template_name = 'pinauth/register.html'

