# coding:utf8
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated

from yaspster import Response
from yapster.models import UserInfo as UserInfoModel
from yapster.models import UserSetting as UserSettingModel
from yapster.models import Friendship
from yapster.serializers import UserInfoSerializer
from yapster.serializers import UserSettingSerializer

from django.contrib.auth.models import User

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

@api_view(['POST'])
def friendships_create(request, followed_id):
    try:
        follower = request.user
        if follower.id == int(followed_id):
            return Response({'detail':'Cannot Follow Yourself'}, status=status.HTTP_501_NOT_IMPLEMENTED)
        obj = Friendship()
        result = obj.create_friendship(follower, followed_id)
        if result:
            return Response({'sucess': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail':'Already Exist'}, status=status.HTTP_501_NOT_IMPLEMENTED)
    except User.DoesNotExist:
        return Response({'detail': 'Users Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def follower_list(request, followed_id):
    try:
        obj = Friendship()
        result = obj.follower_list(followed_id)
        return Response(result)
    except (Friendship.DoesNotExist, User.DoesNotExist):
        return Response({'detail': 'Users Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def destroy_friendship(request, followed_id):
    '''
    remove the friendship tith the user who you don't want to follow
    '''
    try:
        follower = request.user
        obj = Friendship()
        result = obj.destroy_friendship(follower, followed_id)
        if result:
            return Response({'sucess': True}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Failed'}, status=status.HTTP_304_NOT_MODIFIED)

    except (Friendship.DoesNotExist, User.DoesNotExist):
        return Response({'detail': 'Users Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def destroy_follower(request,follower_id):
    '''
    remove the follower who you don't want him to follow you
    '''
    try:
        followed = request.user
        obj = Friendship()
        result = obj.destroy_follower(followed, follower_id)
        if result:
            return Response({'sucess': True}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Failed'}, status=status.HTTP_304_NOT_MODIFIED)

    except (Friendship.DoesNotExist, User.DoesNotExist):
        return Response({'detail': 'Users Not Found'}, status=status.HTTP_404_NOT_FOUND)
