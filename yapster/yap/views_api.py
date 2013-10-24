# coding:utf8
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import OAuth2Authentication

from yapster import _j
from yap.models import Yap as YapModel
from yap.models import Friendship
from yap.models import Listening as ListeningModel
from yap.models import ReYapping as ReYappingModel
from yap.models import Liking as LikingModel
from yap.serializers import CreateYapSerializer
from yap.serializers import YapSerializer
# from yap.serializers import ListeningSerializer
# from yap.serializers import ReYappingSerializer
# from yap.serializers import LikingSerializer


class CreateYap(CreateAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = CreateYapSerializer

    def create(self, request, *args, **kwargs):

        y = YapModel()
        y.user = request.user

        serializer = self.get_serializer(
            data=request.DATA, files=request.FILES, instance=y)

        if serializer.is_valid():
            serializer.save()
            # add tags
            y.add_tags(serializer.data.get('tagstr'))
            headers = self.get_success_headers(serializer.data)
            return Response(
                _j(content={'yap_id': y.id}),
                status=status.HTTP_201_CREATED,
                headers=headers)
        return Response(
            _j(success=False, content=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST)


class Yap(RetrieveUpdateDestroyAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = YapModel.objects.filter(active_flag=True)
    serializer_class = YapSerializer

    def pre_save(self, obj):
        # todo response 403 when update other user's YAP
        obj.user = self.request.user


@api_view(['POST'])
def listen(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.listenedby(request.user)
        return Response(_j(), status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response(_j(message='Not found'), status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def reyap(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.reyapedby(request.user)
        return Response(_j(), status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response(_j(message='Not found'), status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def unreyap(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.unreyapedby(request.user)
        return Response(_j(), status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response(_j(message='Not found'), status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def like(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.likedby(request.user)
        return Response(_j(), status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response(_j(message='Not found'), status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def unlike(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.unlikedby(request.user)
        return Response(_j(), status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response(_j(message='Not found'), status=status.HTTP_404_NOT_FOUND)

# class Listening(RetrieveDestroyAPIView):
#     authentication_classes = (
#         SessionAuthentication, BasicAuthentication, OAuth2Authentication)
#     permission_classes = (IsAuthenticated,)

#     queryset = ListeningModel.objects.filter()
#     serializer_class = ListeningSerializer

# class ReYapping(RetrieveDestroyAPIView):
#     authentication_classes = (
#         SessionAuthentication, BasicAuthentication, OAuth2Authentication)
#     permission_classes = (IsAuthenticated,)
#     queryset = ReYappingModel.objects.filter()
#     serializer_class = ReYappingSerializer
# class Liking(RetrieveDestroyAPIView):
#     authentication_classes = (
#         SessionAuthentication, BasicAuthentication, OAuth2Authentication)
#     permission_classes = (IsAuthenticated,)
#     queryset = LikingModel.objects.filter()
#     serializer_class = LikingSerializer


@api_view(['POST'])
def friendships_create(request, followed_id):
    try:
        follower = request.user
        obj = Friendship()
        result = obj.create_friendship(follower, followed_id)
        if result:
            return Response(_j(), status=status.HTTP_201_CREATED)
        else:
            #l[0] is True
            return Response({'detail': 'Already Exist'}, status=status.HTTP_501_NOT_IMPLEMENTED)
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
def destroy_follower(request, follower_id):
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
