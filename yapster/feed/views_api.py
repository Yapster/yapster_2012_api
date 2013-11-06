# coding:utf8
from django.db.models import Q, F

from rest_framework.generics import ListAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated

from feed.models import Feed
from yap.models import Like, Reyap
from feed.serializers import FeedSerializer


class SelfFeed(ListAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = Feed.objects.filter()
    serializer_class = FeedSerializer

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def get_queryset(self):
        fs = Feed.objects.filter(user=self.request.user,
                                 is_active=True,
                                 is_show=True).order_by('-dateline')
        if self.request.GET.get('pk'):
            fs = fs.filter(pk__gt=self.request.GET.get('pk'))

        for f in fs:
            f.yap.is_liked = False
            f.yap.is_reyapped = False
            if Like.objects.filter(yap=f.yap,
                                   user=self.request.user, is_active=True):
                f.yap.is_liked = True
            if Reyap.objects.filter(yap=f.yap,
                                    user=self.request.user, is_active=True):
                f.yap.is_reyapped = True
        return fs


class Activity(ListAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = Feed.objects.filter()
    serializer_class = FeedSerializer

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def get_queryset(self):
        fs = Feed.objects.filter(
            (Q(user=F('yap_user'), reyap_user__isnull=True)
             | Q(user=F('reyap_user'))),
            user_id=self.kwargs.get('user'),
            is_active=True,
            is_show=True
        ).order_by('-dateline')
        if self.request.GET.get('pk'):
            fs = fs.filter(pk__gt=self.request.GET.get('pk'))
        return fs
