# coding:utf8
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated

from yapster.utils import Response
from users.models import Info as UserInfoModel
from users.models import Setting as UserSettingModel
from users.serializers import UserInfoSerializer
from users.serializers import UserSettingSerializer


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
@permission_classes([IsAuthenticated, ])
def listen(request, pk):
    result = request.user.info.follow(pk)

    http_status = status.HTTP_201_CREATED
    if result == 'Cannot Follow Yourself':
        http_status = status.HTTP_501_NOT_IMPLEMENTED
    elif result == 'Already Exist':
        http_status = status.HTTP_304_NOT_MODIFIED
    elif result == 'User DoesNotExist':
        http_status = status.HTTP_404_NOT_FOUND

    return Response(message=result, status=http_status)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def confirm(request, pk):
    '''
    confirm the followship, allow somebody to listen
    '''
    result = request.user.info.confrim(pk)

    http_status = status.HTTP_200_OK
    if result == 'Friendship DoesNotExist':
        http_status = status.HTTP_404_NOT_FOUND
    return Response(message=result, status=http_status)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def unlisten(request, pk):
    '''
    remove the friendship tith the user who you don't want to follow
    '''
    result = request.user.info.unfollow(pk)

    http_status = status.HTTP_200_OK
    if result == 'Friendship DoesNotExist':
        http_status = status.HTTP_404_NOT_FOUND
    return Response(message=result, status=http_status)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def remove_listener(request, pk):
    '''
    remove the follower who you don't want him to follow you
    '''
    result = request.user.info.remove_follower(pk)

    http_status = status.HTTP_200_OK
    if result == 'Friendship DoesNotExist':
        http_status = status.HTTP_404_NOT_FOUND
    return Response(message=result, status=http_status)


# @api_view(['GET'])
# def follower_list(request, followed_id):
#     try:
#         obj = Friendship()
#         result = obj.follower_list(followed_id)
#         return Response(content=result)
#     except (Friendship.DoesNotExist, User.DoesNotExist):
#         return Response(message='Users Not Found',
#                         status=status.HTTP_404_NOT_FOUND)



# @api_view(['POST'])
# def destroy_follower(request, follower_id):
#     '''
#     remove the follower who you don't want him to follow you
#     '''
#     try:
#         followed = request.user
#         obj = Friendship()
#         result = obj.destroy_follower(followed, follower_id)
#         if result:
#             return Response()
#         else:
#             return Response(message='Failed',
#                             status=status.HTTP_304_NOT_MODIFIED)

#     except (Friendship.DoesNotExist, User.DoesNotExist):
#         return Response(message='Users Not Found',
#                         status=status.HTTP_404_NOT_FOUND)
