# coding:utf8
from rest_framework import serializers
from users.models import Info as UserInfo
from users.models import Setting as UserSetting


class UserInfoSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField()

    class Meta:
        model = UserInfo
        # read_only_fields = ('user',)


class UserSettingSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField()

    class Meta:
        model = UserSetting
        # read_only_fields = ('user',)
