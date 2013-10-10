# coding:utf8
from rest_framework import serializers
from yap.models import Yap


class YapsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Yap
        fields = ('path', 'tags', 'length')
