# coding=utf-8
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from rest_framework import generics
from rest_framework import serializers
from rest_framework import status

from registration.backends.default.views import \
    RegistrationView as NormalRegistrationView
from registration.backends.default.views import \
    ActivationView as NormalActivationView

from yapster import Response


class PostAPIView(generics.CreateAPIView):

    def action(self, request, **cleaned_data):
        """custom action"""
        pass

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.DATA)

        if serializer.is_valid():
            self.action(request, **serializer.data)
            return Response()
        return Response(
            success=False,
            content=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


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
                _("This email address is already in use."))
        return attrs


class RegistrationView(PostAPIView):
    serializer_class = RegistrationSerializer

    def action(self, request, **cleaned_data):
        _n = NormalRegistrationView()
        new_user = _n.register(request, **cleaned_data)
        return new_user


class ActivationSerializer(serializers.Serializer):
    activation_key = serializers.CharField(required=True)


class ActivationView(PostAPIView):
    serializer_class = ActivationSerializer

    def action(self, request, activation_key):
        _n = NormalActivationView()
        return _n.activate(request, activation_key)
