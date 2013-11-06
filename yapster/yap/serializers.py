# coding:utf8
from rest_framework import serializers
from yap.models import Yap
# from yap.models import Listen
# from yap.models import Reyap
# from yap.models import Like


class CreateYapSerializer(serializers.ModelSerializer):
    tagstr = serializers.CharField(required=False)

    class Meta:
        model = Yap
        fields = ('id', 'title', 'path', 'length', 'tagstr')


class YapSerializer(serializers.ModelSerializer):
    tagstr = serializers.RelatedField()
    is_liked = serializers.BooleanField()
    is_reyapped = serializers.BooleanField()

    class Meta:
        model = Yap
        exclude = ('user', 'tags')
