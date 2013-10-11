# coding:utf8
from rest_framework import serializers
from yap.models import Yap


class YapsSerializer(serializers.ModelSerializer):
    tagstr = serializers.CharField()
    
    class Meta:
        model = Yap
        fields = ('path', 'length', 'tagstr')
