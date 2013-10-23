#coding=utf-8
import hashlib

from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView as NormalRegistrationView
from registration.backends.default.views import ActivationView as NormalActivationView

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from yapster.models import UserInfo
from yapster.models import UserSetting


class PostAPIView(generics.CreateAPIView):

    def action(self, request, **cleaned_data):
        """custom action"""
        pass

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            result = self.action(request, **serializer.data)
            headers = self.get_success_headers(serializer.data)
            return Response({'success': True, 'message': None},
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password1 = serializers.CharField(read_only=True)
    password2 = serializers.CharField(read_only=True)

    def validate(self, attrs):
        # Hashes collide, so they are not "100% unique", period.
        attrs['password1'] = attrs['password']
        attrs['password2'] = attrs['password']
        return attrs

    def validate_email(self, attrs, source):
        """
        Check that the blog post is about Django.
        """
        value = attrs[source]
        if User.objects.filter(email__iexact=value):
            raise serializers.ValidationError(
                _("This email address is already in use. Please supply a different email address."))
        return attrs


class RegistrationView(PostAPIView):
    serializer_class = RegistrationSerializer

    def init_user(self, user):
        u = UserInfo()
        u.user = new_user
        u.email = new_user.email
        u.save()

        u = UserSetting()
        u.user = new_user
        u.save()
        return True

    def action(self, request, **cleaned_data):
        new_user = _n.register(request, **cleaned_data)
        if self.init_user(new_user):
            return new_user
        else:
            return None

class ActivationSerializer(serializers.Serializer):
    activation_key = serializers.CharField(required=True)


class ActivationView(PostAPIView):
    serializer_class = ActivationSerializer

    def action(self, request, activation_key):
        _n = NormalActivationView()
        return _n.activate(request, activation_key)