# coding=utf-8
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns
from yap.views_api import CreateYap


urlpatterns = patterns('',
                       url(r'^create/$', CreateYap.as_view()),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
