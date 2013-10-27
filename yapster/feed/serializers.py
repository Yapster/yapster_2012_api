# coding:utf8
from rest_framework import serializers
from feed.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    serialized_yap = serializers.RelatedField()
    # serialized_user = serializers.RelatedField()
    serialized_yap_user = serializers.RelatedField()
    serialized_reyap_user = serializers.RelatedField()

    class Meta:
        model = Feed
        exclude = ('user', 'yap', 'yap_user', 'reyap_user',)
