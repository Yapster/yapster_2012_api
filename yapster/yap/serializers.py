# coding:utf8
from rest_framework import serializers
from yap.models import Yap


class CreateYapSerializer(serializers.ModelSerializer):
    tagstr = serializers.CharField()

    class Meta:
        model = Yap
        fields = ('path', 'length', 'tagstr')


class YapSerializer(serializers.ModelSerializer):
    listening = serializers.RelatedField(many=True)
    reyapping = serializers.RelatedField(many=True)
    liking = serializers.RelatedField(many=True)

    class Meta:
        model = Yap
        exclude = ('user', )


class ListeningSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listening

class ReYappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReYapping

class LikingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Liking
