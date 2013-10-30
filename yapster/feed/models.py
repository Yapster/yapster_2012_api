# coding=utf-8
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from django_rq import enqueue
from yap.models import Yap
from yap.serializers import YapSerializer
from yap.signals import yap_created
from yap.signals import reyap_created
from yap.signals import yap_deleted
from yap.signals import reyap_deleted


class FeedManager(models.Manager):

    def create_by_yap(self, yap):
        followerships = yap.user.followerships.filter(
            is_active=True, is_confirm=True)
        for followership in followerships:
            f = Feed.objects.get_or_create(
                user=followership.follower,
                yap=yap,
                yap_user=yap.user,
                reyap_user=None,
                dateline=yap.dateline
            )
            if not f[1] and not f[0].is_active:
                f[0].is_active = True
                f[0].save()
        # for activities
        f = Feed.objects.get_or_create(
            user=yap.user,
            yap=yap,
            yap_user=yap.user,
            reyap_user=None,
            dateline=yap.dateline
        )
        if not f[1] and not f[0].is_active:
            f[0].is_active = True
            f[0].save()

    def create_by_reyap(self, reyap):
        followerships = reyap.user.followerships.filter(
            is_active=True, is_confirm=True)
        for followership in followerships:
            f = Feed.objects.get_or_create(
                user=followership.follower,
                yap=reyap.yap,
                yap_user=reyap.yap.user,
                reyap_user=reyap.user,
            )
            if not f[1]:
                f[0].dateline = reyap.dateline
                if not f[0].is_active:
                    f[0].is_active = True
                f[0].save()

        # for activities
        f = Feed.objects.get_or_create(
            user=reyap.user,
            yap=reyap.yap,
            yap_user=reyap.yap.user,
            reyap_user=reyap.user
        )
        if not f[1]:
            f[0].dateline = reyap.dateline
            if not f[0].is_active:
                f[0].is_active = True
            f[0].save()

    def delete_by_yap(self, yap):
        self.filter(yap=yap).update(is_active=False)

    def delete_by_reyap(self, reyap):
        self.filter(reyap_user=reyap.user, yap=reyap.yap).update(
            is_active=False)


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

    class Meta:
        unique_together = ('user', 'yap', 'yap_user', 'reyap_user')

    def delete(self):
        self.is_active = False
        self.save()

    def hide(self):
        self.is_show = False
        self.save()

    def serialized_yap(self):
        y = YapSerializer(instance=self.yap)
        return y.data

    def serialized_user(self):
        u = UserInfoSerializer(instance=self.user.info)
        return u.data

    def serialized_yap_user(self):
        u = UserInfoSerializer(instance=self.yap_user.info)
        return u.data

    def serialized_reyap_user(self):
        if self.reyap_user:
            u = UserInfoSerializer(instance=self.reyap_user.info)
            return u.data
        return None


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
    enqueue(Feed.objects.create_by_reyap, reyap)


@receiver(reyap_deleted)
def reyap_delete_feed(sender, **kwargs):
    reyap = kwargs.get('reyap', None)
    enqueue(Feed.objects.delete_by_reyap, reyap)


from users.serializers import UserInfoSerializer
