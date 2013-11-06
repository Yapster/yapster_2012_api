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

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        is_created = False
        if not self.pk:
            is_created = True
        super(Yap, self).save(*args, **kwargs)
        if is_created:
            signals.yap_created.send(sender=self.__class__,
                                     yap=self)
        return True

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()
            signals.yap_created.send(sender=self.__class__,
                                     yap=self)
            return True
        else:
            return False

    def delete(self):
        if self.is_active:
            self.is_active = False
            self.save()
            signals.yap_deleted.send(sender=self.__class__,
                                     yap=self)
            return True
        else:
            return False

    def add_tags(self, tag_str):
        tags = tag_str.split(',')
        for tag in tags:
            t = Tag.objects.get_or_create(tagname=tag)
            self.tags.add(t[0])

    def tagstr(self):
        return ','.join([tag.tagname for tag in self.tags.filter()])

    def reyapedby(self, user):
        obj = Reyap.objects.get_or_create(yap=self, user=user)
        if not obj[1]:
            obj[0].activate()
        return obj[0]

    def unreyapedby(self, user):
        obj = Reyap.objects.get(yap=self, user=user)
        obj.delete()
        return True

    def listenedby(self, user):
        obj = Listen()
        obj.yap = self
        obj.user = user
        obj.save()
        self.listen_count += 1
        self.save()
        return obj

    def likedby(self, user):
        obj = Like.objects.get_or_create(yap=self, user=user)
        if not obj[1]:
            obj[0].activate()
        return obj[0]

    def unlikedby(self, user):
        obj = Like.objects.get(yap=self, user=user)
        obj.delete()
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
        is_created = False
        if not self.pk:
            is_created = True
        super(Reyap, self).save(*args, **kwargs)

        if is_created:
            self.yap.reyap_count += 1
            self.yap.save()
            signals.reyap_created.send(sender=self.__class__,
                                       reyap=self)
        return True

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

            self.yap.reyap_count += 1
            self.yap.save()
            signals.reyap_created.send(sender=self.__class__,
                                       reyap=self)
            return True
        else:
            return False

    def delete(self):
        if self.is_active:
            self.is_active = False
            self.save()

            self.yap.reyap_count -= 1
            self.yap.save()
            signals.reyap_deleted.send(sender=self.__class__,
                                       reyap=self)
            return True
        else:
            return False


class Like(models.Model):
    yap = models.ForeignKey(Yap, related_name='likes')
    user = models.ForeignKey(User, related_name='likes')
    is_active = models.BooleanField(default=True)
    dateline = models.DateTimeField(auto_now_add=True)

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

            self.yap.like_count += 1
            self.yap.save()
            return True
        else:
            return False

    def delete(self):
        if self.is_active:
            self.is_active = False
            self.save()

            self.yap.like_count -= 1
            self.yap.save()
            return True
        else:
            return False
