# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	SingleUseToken,
)


class SingleUseTokenCreateView(CreateView):

    model = SingleUseToken


class SingleUseTokenDeleteView(DeleteView):

    model = SingleUseToken


class SingleUseTokenDetailView(DetailView):

    model = SingleUseToken


class SingleUseTokenUpdateView(UpdateView):

    model = SingleUseToken


class SingleUseTokenListView(ListView):

    model = SingleUseToken

