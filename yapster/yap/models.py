# coding:utf8
import datetime

from django.db import models
from django.contrib.auth.models import User
# from taggit.managers import TaggableManager


class Tag(models.Model):
    tagname = models.CharField(max_length=30, null=False)


class Yap(models.Model):
    user = models.ForeignKey(User, related_name='yaps')
    path = models.CharField(
        max_length=255, null=False, verbose_name='audio path')
    tags = models.ManyToManyField(Tag, blank=True)
    length = models.IntegerField(default=0)
    active_flag = models.BooleanField(default=True)

    listen_count = models.IntegerField(default=0)
    re_yap_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    # yapster_latitude = models.FloatField(blank=True, null=True)
    # yapster_longitude = models.FloatField(blank=True, null=True)

    def add_tags(self, tag_str):
        tags = tag_str.split(',')
        for tag in tags:
            t = Tag.objects.get_or_create(tagname=tag)
            self.tags.add(t[0])
        # self.save()
