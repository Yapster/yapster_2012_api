# coding:utf8
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated

from yapster.models import UserInfo as UserInfoModel
from yapster.models import UserSetting as UserSettingModel
from yapster.serializers import UserInfoSerializer
from yapster.serializers import UserSettingSerializer



class SelfInfo(RetrieveUpdateAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = UserInfoModel.objects.filter(user__is_active=True)
    serializer_class = UserInfoSerializer

    def get_object(self, queryset=None):
        return self.queryset.get(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user


class SelfSetting(RetrieveUpdateAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = UserSettingModel.objects.filter(user__is_active=True)
    serializer_class = UserSettingSerializer

    def get_object(self, queryset=None):
        return self.queryset.get(user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user


class UserInfo(RetrieveAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = UserInfoModel.objects.filter(user__is_active=True)
    serializer_class = UserInfoSerializer


class UserSetting(RetrieveAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = UserSettingModel.objects.filter(user__is_active=True)
    serializer_class = UserSettingSerializer