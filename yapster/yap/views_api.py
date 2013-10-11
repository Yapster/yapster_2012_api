# coding:utf8
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from yap.models import Yap
from yap.serializers import YapsSerializer


class CreateYap(CreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = YapsSerializer

    def create(self, request, *args, **kwargs):
        y = Yap()
        y.user = request.user

        serializer = self.get_serializer(
            data=request.DATA, files=request.FILES, instance=y)

        if serializer.is_valid():
            serializer.save()
            y.add_tags(serializer.data.get('tagstr'))
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
