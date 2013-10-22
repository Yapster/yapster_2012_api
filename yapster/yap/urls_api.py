# coding=utf-8
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns
from yap.views_api import CreateYap
from yap.views_api import Yap
from yap.views_api import Listening
from yap.views_api import ReYapping
from yap.views_api import Liking

urlpatterns = patterns('yap.views_api',
                       url(r'^create/$', CreateYap.as_view()),
                       url(r'^(?P<pk>[0-9]+)/$', Yap.as_view()),
                       url(r'^add_listening/(?P<pk>[0-9]+)/$', 'add_listening'),
                       url(r'^add_reyapping/(?P<pk>[0-9]+)/$', 'add_reyapping'),
                       url(r'^add_liking/(?P<pk>[0-9]+)/$', 'add_liking'),
                       url(r'^listening/(?P<pk>[0-9]+)/$',
                           Listening.as_view()),
                       url(r'^reyapping/(?P<pk>[0-9]+)/$',
                           ReYapping.as_view()),
                       url(r'^liking/(?P<pk>[0-9]+)/$',
                           Liking.as_view()),
                       url(r'^listener/(?P<pk>\d+)/$', 'listener_request')
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
