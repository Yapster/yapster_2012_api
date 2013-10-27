# coding:utf8
from rest_framework import serializers
from feed.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField()
    yap = serializers.RelatedField()
    yap_user = serializers.RelatedField()
    reyap_user = serializers.RelatedField()

    class Meta:
        model = Feed
        exclude = ('user', )
