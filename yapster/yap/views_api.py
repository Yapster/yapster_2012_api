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
from yap.serializers import CreateYapSerializer
from yap.serializers import YapSerializer


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
def listening(request, pk):
    try:
        yap = YapModel.objects.get(pk=pk)
        yap.add_listening(request.user)
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    except YapModel.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', ])
def reyapping(request, pk):
    pass


@api_view(['POST', ])
def liking(request, pk):
    pass
