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
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, OAuth2Authentication
from rest_framework.permissions import IsAuthenticated

from yapster.models import UserInfo


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
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(read_only=True)

    def validate(self, attrs):
        # Hashes collide, so they are not "100% unique", period.
        attrs['username'] = hashlib.md5(
            attrs['email']).digest().encode('base64')[:-1]
        attrs['password2'] = attrs['password1']
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

    def action(self, request, **cleaned_data):
        _n = NormalRegistrationView()
        return _n.register(request, **cleaned_data)


class ActivationSerializer(serializers.Serializer):
    activation_key = serializers.CharField(required=True)


class ActivationView(PostAPIView):
    serializer_class = ActivationSerializer

    def action(self, request, activation_key):
        _n = NormalActivationView()
        return _n.activate(request, activation_key)


class UserInfoSerializer(serializers.Serializer):
    handle = serializers.CharField(required=True)
    phone = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)


class UserInfoView(PostAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer

    def action(self, request, **cleaned_data):
        u = UserInfo()
        u.user = request.user
        u.handle = cleaned_data['handle']
        u.phone = cleaned_data['phone']
        u.first_name = cleaned_data['first_name']
        u.last_name = cleaned_data['last_name']
        u.email = u.user.email
        u.user.first_name = cleaned_data['first_name']
        u.user.last_name = cleaned_data['last_name']
        u.user.save()
        u.save()
        return u