# coding:utf8
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import OAuth2Authentication

from yapster.utils import Response
from yap.models import Yap as YapModel
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
            data=request.DATA, instance=y)

        if serializer.is_valid():
            serializer.save()
            y.add_tags(request.POST.get('tagstr', ''))
            # headers = self.get_success_headers(serializer.data)
            return Response(content=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(success=False, content=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class Yap(RetrieveUpdateDestroyAPIView):
    authentication_classes = (
        SessionAuthentication, BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    queryset = YapModel.objects.filter(is_active=True)
    serializer_class = YapSerializer

    def pre_save(self, obj):
        # todo response 403 when update other user's YAP
        obj.user = self.request.user


@api_view(['POST'])
def listen(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.listenedby(request.user)
        return Response(status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response(success=False,
                        message='Not found', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def reyap(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.reyapedby(request.user)
        return Response(status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response(success=False,
                        message='Not found', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def unreyap(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.unreyapedby(request.user)
        return Response(status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response(success=False,
                        message='Not found', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def like(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.likedby(request.user)
        return Response(status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response(success=False,
                        message='Not found', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def unlike(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.unlikedby(request.user)
        return Response(status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response(success=False,
                        message='Not found',
                        status=status.HTTP_404_NOT_FOUND)

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
