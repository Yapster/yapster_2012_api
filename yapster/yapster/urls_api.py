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
)

# urlpatterns = format_suffix_patterns(urlpatterns)
