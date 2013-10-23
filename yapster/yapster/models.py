from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserInfo(models.Model):
    user = models.OneToOneField(User, verbose_name='auth_user')

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)


class UserSetting(models.Model):
    user = models.OneToOneField(User, verbose_name='auth_user')

    need_permission_to_listen = models.BooleanField(
        default=False, verbose_name='need permission to listen')
    need_permission_to_message = models.BooleanField(
        default=False,  verbose_name='need permission to msg')

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
