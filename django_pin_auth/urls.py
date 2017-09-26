# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(
        regex="^SingleUseToken/~create/$",
        view=views.SingleUseTokenCreateView.as_view(),
        name='SingleUseToken_create',
    ),
    url(
        regex="^SingleUseToken/(?P<pk>\d+)/~delete/$",
        view=views.SingleUseTokenDeleteView.as_view(),
        name='SingleUseToken_delete',
    ),
    url(
        regex="^SingleUseToken/(?P<pk>\d+)/$",
        view=views.SingleUseTokenDetailView.as_view(),
        name='SingleUseToken_detail',
    ),
    url(
        regex="^SingleUseToken/(?P<pk>\d+)/~update/$",
        view=views.SingleUseTokenUpdateView.as_view(),
        name='SingleUseToken_update',
    ),
    url(
        regex="^SingleUseToken/$",
        view=views.SingleUseTokenListView.as_view(),
        name='SingleUseToken_list',
    ),
	]
