# coding=utf-8
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from django_rq import enqueue
from yap.models import Yap
from yap.signals import yap_created
from yap.signals import reyap_created
from yap.signals import yap_deleted
from yap.signals import reyap_deleted


class FeedManager(models.Manager):

    def create_by_yap(self, yap):
        followerships = yap.user.followerships.filter(
            is_active=True, is_confirm=True)
        for followership in followerships:
            Feed(
                user=followership.follower,
                yap=yap,
                yap_user=yap.user
            ).save()

    def create_by_reyap(self, reyap):
        followerships = reyap.user.followerships.filter(
            is_active=True, is_confirm=True)
        for followership in followerships:
            Feed(
                user=followership.follower,
                yap=reyap.yap,
                yap_user=reyap.yap.user,
                reyap_user=reyap.user
            ).save()

    def delete_by_yap(self, yap):
        self.filter(yap=yap).update(is_active=False)

    def delete_by_reyap(self, reyap):
        self.filter(reyap=reyap).update(is_active=False)


class Feed(models.Model):
    user = models.ForeignKey(User, verbose_name='user', related_name='feeds')
    yap = models.ForeignKey(Yap, verbose_name='yap')
    yap_user = models.ForeignKey(
        User, verbose_name='yap user', related_name='feeds_yap')
    reyap_user = models.ForeignKey(
        User, verbose_name='reyap user', null=True, blank=True,
        related_name='feeds_reyap')
    dateline = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_show = models.BooleanField(default=True)

    objects = FeedManager()

    def delete(self):
        self.is_active = False
        self.save()

    def hide(self):
        self.is_show = False
        self.save()


@receiver(yap_created)
def yap_create_feed(sender, **kwargs):
    yap = kwargs.get('yap', None)
    enqueue(Feed.objects.create_by_yap, yap)


@receiver(yap_deleted)
def yap_delete_feed(sender, **kwargs):
    yap = kwargs.get('yap', None)
    enqueue(Feed.objects.delete_by_yap, yap)


@receiver(reyap_created)
def reyap_create_feed(sender, **kwargs):
    reyap = kwargs.get('reyap', None)
    enqueue(Feed.objects.create_by_yap, reyap)


@receiver(reyap_deleted)
def reyap_delete_feed(sender, **kwargs):
    reyap = kwargs.get('reyap', None)
    enqueue(Feed.objects.delete_by_reyap, reyap)
