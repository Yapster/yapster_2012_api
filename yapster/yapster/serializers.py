# coding:utf8
from rest_framework import serializers
from yapster.models import UserInfo
from yapster.models import UserSetting


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        exclude = ('user', )


class UserSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSetting
        exclude = ('user', )
