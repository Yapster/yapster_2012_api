# coding:utf8
import datetime

from django.db import models
from django.contrib.auth.models import User
# from taggit.managers import TaggableManager


class Tag(models.Model):
    tagname = models.CharField(max_length=30, null=False)

    def __unicode__(self):
        return self.tagname


class Yap(models.Model):
    user = models.ForeignKey(User, related_name='yaps')
    title = models.CharField(max_length=50, null=False, verbose_name='title')
    path = models.CharField(
        max_length=255, null=False, verbose_name='audio path')
    tags = models.ManyToManyField(Tag, blank=True)
    length = models.IntegerField(default=0)
    active_flag = models.BooleanField(default=True)

    listening_count = models.IntegerField(default=0)
    reyapping_count = models.IntegerField(default=0)
    liking_count = models.IntegerField(default=0)

    dateline = models.DateTimeField(auto_now_add=True)

    def add_tags(self, tag_str):
        tags = tag_str.split(',')
        for tag in tags:
            t = Tag.objects.get_or_create(tagname=tag)
            self.tags.add(t[0])

    def delete(self):
        self.active_flag = False
        self.save()

    def listenedby(self, user):
        obj = Listening()
        obj.yap = self
        obj.listening_user = user
        obj.save()
        self.listening_count += 1
        self.save()
        return obj

    def reyapedby(self, user):
        obj = ReYapping()
        obj.yap = self
        obj.reyapping_user = user
        obj.save()
        self.reyapping_count += 1
        self.save()
        return obj

    def likedby(self, user):
        obj = Liking.objects.get_or_create(yap=self, liking_user=user)
        if obj[1]:
            self.liking_count += 1
            self.save()
        return obj

    def remove_listening(self, pk):
        obj = Listening.objects.get(pk=pk)
        obj.delete()
        return True

    def remove_reyapping(self, pk):
        obj = ReYapping.objects.get(pk=pk)
        obj.delete()
        return True

    def remove_liking(self, pk):
        obj = Liking.objects.get(pk=pk)
        obj.delete()
        return True


class Listening(models.Model):
    yap = models.ForeignKey(Yap, related_name='listening')
    listening_user = models.ForeignKey(User, related_name='listening')
    dateline = models.DateTimeField(auto_now_add=True)


class ReYapping(models.Model):
    yap = models.ForeignKey(Yap, related_name='reyapping')
    reyapping_user = models.ForeignKey(User, related_name='reyapping')
    dateline = models.DateTimeField(auto_now_add=True)


class Liking(models.Model):
    yap = models.ForeignKey(Yap, related_name='liking')
    liking_user = models.ForeignKey(User, related_name='liking')
    dateline = models.DateTimeField(auto_now_add=True)


class Friendship(models.Model):
    followed = models.ForeignKey(User,related_name='friendship_followed')
    follower = models.ForeignKey(User,related_name='firendship_follower')
    dateline = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_friendship(cls, follower, followed_id):
        followed = User.objects.get(pk=followed_id)
        obj = cls.objects.get_or_create(followed=followed, follower=follower)
        return obj[1]
    @classmethod
    def follower_list(cls, followed_id):
        objs = cls.objects.filter(followed=followed_id)

        #temporary test
        followers_id=[]
        for obj in objs:
            followers_id.append(obj.follower_id)
        return followers_id

    @classmethod
    def destroy_friendship(cls, follower, followed_id):
        followed = User.objects.get(pk=followed_id)
        obj = cls.objects.get(followed=followed, follower=follower)
        obj.delete()
        return True

    @classmethod
    def destroy_follower(cls, followed, follower_id):
        follower = User.objects.get(pk=follower_id)
        obj = cls.objects.get(followed=followed, follower=follower)
        obj.delete()
        return True
