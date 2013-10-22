# coding:utf8
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import OAuth2Authentication

from yap.models import Yap as YapModel
from yap.models import ListeningModel
from yap.models import ReYappingModel
from yap.models import LikingModel
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
            return Response(serializer.data, status=status.HTTP_201_CREATED,
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


@api_view(['POST', 'GET'])
def add_listening(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.add_listening(request.user)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class Listening(RetrieveDestroyAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = ListeningModel.objects.filter(active_flag=True)
    serializer_class = ListeningSerializer


@api_view(['POST', 'GET'])
def add_reyapping(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.add_reyapping(request.user)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class ReYapping(RetrieveDestroyAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = ReYappingModel.objects.filter(active_flag=True)
    serializer_class = ReYappingSerializer


@api_view(['POST', 'GET'])
def add_liking(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.add_liking(request.user)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class Liking(RetrieveDestroyAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = LikingModel.objects.filter(active_flag=True)
    serializer_class = LikingSerializer
