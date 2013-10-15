# coding=utf-8
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns
from yap.views_api import CreateYap, Yap


urlpatterns = patterns('yap.views_api',
                       url(r'^create/$', CreateYap.as_view()),
                       url(r'^(?P<pk>[0-9]+)/$', Yap.as_view()),
                       url(r'^listening/(?P<pk>[0-9]+)/$', 'listening'),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
