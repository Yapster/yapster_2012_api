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
    is_active = models.BooleanField(default=True)

    listen_count = models.IntegerField(default=0)
    reyap_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

    dateline = models.DateTimeField(auto_now_add=True)

    def add_tags(self, tag_str):
        tags = tag_str.split(',')
        for tag in tags:
            t = Tag.objects.get_or_create(tagname=tag)
            self.tags.add(t[0])

    def delete(self):
        self.is_active = False
        self.save()

    def listenedby(self, user):
        obj = Listen()
        obj.yap = self
        obj.listen_user = user
        obj.save()
        self.listen_count += 1
        self.save()
        return obj

    def reyapedby(self, user):
        obj = ReYap.objects.get_or_create(yap=self, reyap_user=user)
        if not obj[1]:
            obj[0].is_active = True
            obj[0].save()
        self.reyap_count += 1
        self.save()
        return obj

    def unreyapedby(self, user):
        obj = ReYap.objects.get(yap=self, reyap_user=user)
        obj.delete()
        self.reyap_count -= 1
        self.save()
        return obj

    def likedby(self, user):
        obj = Like.objects.get_or_create(yap=self, like_user=user)
        if not obj[1]:
            obj[0].is_active = True
            obj[0].save()
        self.like_count += 1
        self.save()
        return obj

    def unlikedby(self, user):
        obj = Like.objects.get(yap=self, like_user=user)
        obj.delete()
        self.like_count -= 1
        self.save()
        return True


class Listen(models.Model):
    yap = models.ForeignKey(Yap, related_name='listening')
    listen_user = models.ForeignKey(User, related_name='listening')
    dateline = models.DateTimeField(auto_now_add=True)


class Reyap(models.Model):
    yap = models.ForeignKey(Yap, related_name='reyapping')
    reyap_user = models.ForeignKey(User, related_name='reyapping')
    is_active = models.BooleanField(default=True)
    dateline = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.is_active = False
        self.save()


class Like(models.Model):
    yap = models.ForeignKey(Yap, related_name='liking')
    like_user = models.ForeignKey(User, related_name='liking')
    is_active = models.BooleanField(default=True)
    dateline = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.is_active = False
        self.save()



class FriendshipManager(models.Manager):
    def create():
        pass

    def destroy():
        pass
        

class Friendship(models.Model):
    followed = models.ForeignKey(User, related_name='friendship_followed')
    follower = models.ForeignKey(User, related_name='firendship_follower')
    dateline = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_friendship(cls, follower, followed_id):
        followed = User.objects.get(pk=followed_id)
        obj = cls.objects.get_or_create(followed=followed, follower=follower)
        return obj[1]

    @classmethod
    def follower_list(cls, followed_id):
        objs = cls.objects.filter(followed=followed_id)

        # temporary test
        followers_id = []
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
