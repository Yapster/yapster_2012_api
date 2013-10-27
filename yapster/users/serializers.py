# coding:utf8
# from django.contrib.auth.models import User

from rest_framework import serializers
from users.models import Info as UserInfo
from users.models import Setting as UserSetting


# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         exclude = ('password', 'is_superuser',
#                    'is_staff', 'groups', 'user_permissions')
#         # read_only_fields = ('user',)


class UserInfoSerializer(serializers.ModelSerializer):
    # serialized_user = serializers.RelatedField()

    class Meta:
        model = UserInfo
        # read_only_fields = ('user',)


class UserSettingSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField()

    class Meta:
        model = UserSetting
        # read_only_fields = ('user',)
