# coding=utf-8
from django.conf.urls import patterns, url

# from rest_framework.urlpatterns import format_suffix_patterns
from users.views_api import SelfInfo
from users.views_api import SelfSetting
from users.views_api import UserInfo
from users.views_api import UserSetting
from users.views_api import InfoList

urlpatterns = patterns('users.views_api',
                       url(r'^userlist/$', InfoList.as_view()),
                       url(r'^userinfo/$', SelfInfo.as_view()),
                       url(r'^usersetting/$', SelfSetting.as_view()),
                       url(r'^userinfo/(?P<pk>\d+)/$', UserInfo.as_view()),
                       url(r'^usersetting/(?P<pk>\d+)/$',UserSetting.as_view()),
                       url(r'^listen/(?P<pk>\d+)/$', 'listen'),
                       url(r'^confirm/(?P<pk>\d+)/$', 'confirm'),
                       url(r'^unlisten/(?P<pk>\d+)/$', 'unlisten'),
                       url(r'^remove_listener/(?P<pk>\d+)/$', 'remove_listener')
                       )

# urlpatterns = format_suffix_patterns(urlpatterns)
