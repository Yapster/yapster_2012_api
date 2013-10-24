# coding=utf-8
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns
from yapster.views_api import SelfInfo
from yapster.views_api import SelfSetting
from yapster.views_api import UserInfo
from yapster.views_api import UserSetting

urlpatterns = patterns('yapster.views_api',
                       url(r'^userinfo/$', SelfInfo.as_view()),
                       url(r'^usersetting/$', SelfSetting.as_view()),
                       url(r'^userinfo/(?P<pk>[0-9]+)/$', UserInfo.as_view()),
                       url(r'^usersetting/(?P<pk>[0-9]+)/$', UserSetting.as_view()),
                       url(r'^friendships/create/(?P<followed_id>\d+)/$', 'friendships_create'),
                       url(r'^friendships/followers/list/(?P<followed_id>\d+)/$', 'follower_list'),
                       url(r'^friendships/destroy/(?P<followed_id>\d+)/$','destroy_friendship'),
                       url(r'^friendships/followers/destroy/(?P<follower_id>\d+)/$', 'destroy_follower')
)

# urlpatterns = format_suffix_patterns(urlpatterns)
