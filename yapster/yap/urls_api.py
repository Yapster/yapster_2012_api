# coding=utf-8
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns
from yap.views_api import CreateYap
from yap.views_api import Yap
# from yap.views_api import Listening
# from yap.views_api import ReYapping
# from yap.views_api import Liking

urlpatterns = patterns('yap.views_api',
                       url(r'^create/$', CreateYap.as_view()),
                       url(r'^(?P<pk>[0-9]+)/$', Yap.as_view()),
                       url(r'^listen/(?P<pk>[0-9]+)/$', 'listen'),
                       url(r'^reyap/(?P<pk>[0-9]+)/$', 'reyap'),
                       url(r'^unreyap/(?P<pk>[0-9]+)/$', 'unreyap'),
                       url(r'^like/(?P<pk>[0-9]+)/$', 'like'),
                       url(r'^unlike/(?P<pk>[0-9]+)/$', 'unlike'),
                       # url(r'^(?P<pk>[0-9]+)/listening/$',
                       #     Listening.as_view()),
                       # url(r'^(?P<pk>[0-9]+)/reyapping/$',`
                       #     ReYapping.as_view()),
                       # url(r'^(?P<pk>[0-9]+)/liking/$',
                       #     Liking.as_view()),
                       url(r'^friendships/create/(?P<followed_id>\d+)/$',
                           'friendships_create'),
                       url(r'^friendships/followers/list/(?P<followed_id>\d+)/$', 'follower_list'),
                       url(r'^friendships/destroy/(?P<followed_id>\d+)/$',
                           'destroy_friendship'),
                       url(r'^friendships/followers/destroy/(?P<follower_id>\d+)/$', 'destroy_follower'))

# urlpatterns = format_suffix_patterns(urlpatterns)
