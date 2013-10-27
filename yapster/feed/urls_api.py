# coding=utf-8
from django.conf.urls import patterns, url

# from rest_framework.urlpatterns import format_suffix_patterns
from feed.views_api import SelfFeed

urlpatterns = patterns('feed.views_api',
                       url(r'^$|list/$', SelfFeed.as_view()),
                       )

# urlpatterns = format_suffix_patterns(urlpatterns)
