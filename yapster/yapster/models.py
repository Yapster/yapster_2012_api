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
