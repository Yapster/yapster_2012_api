from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Info(models.Model):
    user = models.OneToOneField(User, verbose_name='auth_user')

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)

    avatar_path = models.CharField(
        _('avatar path'), max_length=255, blank=True)
    background_path = models.CharField(
        _('background path'), max_length=255, blank=True)

    def serialized_user(self):
        u = UserSerializer(instance=self.user)
        return u.data

    def followers(self):
        objs = self.user.followerships.filter(
            is_active=True, is_confirm=True)
        # temporary test
        followers_id = []
        for obj in objs:
            followers_id.append(obj.follower_id)
        return followers_id

    def followeds(self):
        objs = self.user.followedships.filter(
            is_active=True, is_confirm=True)
        # temporary test
        followeds_id = []
        for obj in objs:
            followeds_id.append(obj.followed_id)
        return followeds_id

    def follow(self, followed_id):
        follower = self.user
        if follower.id == int(followed_id):
            return 'Cannot Follow Yourself'
        try:
            followed = User.objects.get(pk=followed_id)
        except User.DoesNotExist:
            return 'User DoesNotExist'
        obj = Friendship.objects.get_or_create(
            followed=followed, follower=follower)
        if obj[1]:
            if followed.setting.need_permission_to_listen:
                obj[0].is_confirm = False
                obj[0].save()
            else:
                obj[0].active_dateline = obj[0].dateline
                obj[0].save()
            return 'Success'
        else:
            if not obj[0].is_active:
                obj[0].is_active = True
                obj[0].save()
                return 'Success'
            else:
                return 'Already Exist'

    def confirm(self, follower_id):
        try:
            obj = self.user.followerships.get(follower_id=follower_id)
            obj.confirm()
            return 'Success'
        except Friendship.DoesNotExist:
            return 'Friendship DoesNotExist'

    def unfollow(self, followed_id):
        try:
            obj = self.user.followedships.get(
                followed_id=followed_id)
            obj.delete()
            return 'Success'
        except Friendship.DoesNotExist:
            return 'Friendship DoesNotExist'

    def remove_follower(self, follower_id):
        try:
            obj = self.user.followerships.get(
                follower_id=follower_id)
            obj.delete()
            return 'Success'
        except Friendship.DoesNotExist:
            return 'Friendship DoesNotExist'


@receiver(post_save, sender=User)
def user_create_info(sender, **kwargs):
    if kwargs.get('created'):
        i = kwargs.get('instance')
        info = Info(
            user=i,
            first_name=i.first_name,
            last_name=i.last_name,
            email=i.email,
            phone='',
            avatar_path='',
            background_path=''
        )
        info.save()
    else:
        i = kwargs.get('instance')
        info = Info.objects.get(user=i)
        info.first_name = i.first_name
        info.last_name = i.last_name
        info.email = i.email
        info.save()


class Setting(models.Model):
    user = models.OneToOneField(User, verbose_name=_('auth_user'))
    need_permission_to_listen = models.BooleanField(
        default=False, verbose_name=_('need permission to listen'))
    need_permission_to_message = models.BooleanField(
        default=False,  verbose_name=_('need permission to msg'))


@receiver(post_save, sender=User)
def user_create_setting(sender, **kwargs):
    if kwargs.get('created'):
        i = kwargs.get('instance')
        setting = Setting(
            user=i,
            need_permission_to_message=False,
            need_permission_to_listen=False
        )
        setting.save()


class Friendship(models.Model):
    followed = models.ForeignKey(User, related_name='followerships')
    follower = models.ForeignKey(User, related_name='followedships')
    dateline = models.DateTimeField(auto_now_add=True)
    is_confirm = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    active_dateline = models.DateTimeField(blank=True, null=True)

    def confirm(self):
        '''only followed user has permission'''
        self.is_confirm = True
        self.save()

    def delete(self):
        '''followed and follower user both have permission'''
        self.is_active = False
        self.save()


from users.serializers import UserSerializer
