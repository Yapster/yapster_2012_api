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

from yap.models import Yap as YapModel
from yap.models import Listening as ListeningModel
from yap.models import ReYapping as ReYappingModel
from yap.models import Liking as LikingModel
from yap.serializers import CreateYapSerializer
from yap.serializers import YapSerializer
from yap.serializers import ListeningSerializer
from yap.serializers import ReYappingSerializer
from yap.serializers import LikingSerializer


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
                {'success': True, 'content': {'yap_id': y.id}}, status=status.HTTP_201_CREATED,
                headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Yap(RetrieveUpdateDestroyAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = YapModel.objects.filter(active_flag=True)
    serializer_class = YapSerializer

    def pre_save(self, obj):
        obj.user = self.request.user


@api_view(['POST'])
def listen(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.listenedby(request.user)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class Listening(RetrieveDestroyAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = ListeningModel.objects.filter()
    serializer_class = ListeningSerializer


@api_view(['POST'])
def reyap(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.reyapedby(request.user)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class ReYapping(RetrieveDestroyAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = ReYappingModel.objects.filter()
    serializer_class = ReYappingSerializer


@api_view(['POST'])
def like(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.likedby(request.user)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class Liking(RetrieveDestroyAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = LikingModel.objects.filter()
    serializer_class = LikingSerializer


@api_view(['POST', 'GET'])
def listener_request(request, pk):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    if request.method == 'POST':
        listener = request.user
        listened = User.objects.get(pk=pk)
        l = ListenerRequest.objects.get_or_create(
            listener=listener, listened=listened)
        if l[1]:
            return Response({'sucess': True}, status=status.HTTP_201_CREATED)
        else:
            #l[0] is True
            return Response({'detail': 'Already Exist'}, status=status.HTTP_501_NOT_IMPLEMENTED)

    if request.method == 'GET':
        # get listener
        try:
            user = User.objects.get(pk=pk)
            listeners = ListenerRequest.objects.filter(listened=user)
            listener_id = []
            for listener in listeners:
                listener_id.append(listener.listener_id)
            return Response(listener_id)
        except User.DoesNotExist:
            return Response({'detail': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
