# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

from yap import signals


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

    def save(self, *args, **kwargs):
        super(Yap, self).save(*args, **kwargs)
        signals.yap_created.send(sender=self.__class__,
                                 yap=self)

    def delete(self):
        self.is_active = False
        self.save()
        signals.yap_deleted.send(sender=self.__class__,
                                 yap=self)

    def add_tags(self, tag_str):
        tags = tag_str.split(',')
        for tag in tags:
            t = Tag.objects.get_or_create(tagname=tag)
            self.tags.add(t[0])

    def listenedby(self, user):
        obj = Listen()
        obj.yap = self
        obj.user = user
        obj.save()
        self.listen_count += 1
        self.save()
        return obj

    def reyapedby(self, user):
        obj = Reyap.objects.get_or_create(yap=self, user=user)
        if not obj[1] and not obj[0].is_active:
            obj[0].is_active = True
            obj[0].save()
            self.reyap_count += 1
            self.save()
        elif obj[1]:
            self.reyap_count += 1
            self.save()
        else:
            return None
        return obj[0]

    def unreyapedby(self, user):
        obj = Reyap.objects.get(yap=self, user=user)
        obj.delete()
        self.reyap_count -= 1
        self.save()
        return obj

    def likedby(self, user):
        obj = Like.objects.get_or_create(yap=self, user=user)
        if not obj[1] and not obj[0].is_active:
            obj[0].is_active = True
            obj[0].save()
            self.like_count += 1
            self.save()
        elif obj[1]:
            self.like_count += 1
            self.save()
        else:
            return None
        return obj[0]

    def unlikedby(self, user):
        obj = Like.objects.get(yap=self, user=user)
        obj.delete()
        self.like_count -= 1
        self.save()
        return True


class Listen(models.Model):
    yap = models.ForeignKey(Yap, related_name='listens')
    user = models.ForeignKey(User, related_name='listens')
    dateline = models.DateTimeField(auto_now_add=True)


class Reyap(models.Model):
    yap = models.ForeignKey(Yap, related_name='reyaps')
    user = models.ForeignKey(User, related_name='reyaps')
    is_active = models.BooleanField(default=True)
    dateline = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Reyap, self).save(*args, **kwargs)
        signals.reyap_created.send(sender=self.__class__,
                                   reyap=self)

    def delete(self):
        self.is_active = False
        self.save()
        signals.reyap_deleted.send(sender=self.__class__,
                                   reyap=self)


class Like(models.Model):
    yap = models.ForeignKey(Yap, related_name='likes')
    user = models.ForeignKey(User, related_name='likes')
    is_active = models.BooleanField(default=True)
    dateline = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.is_active = False
        self.save()
