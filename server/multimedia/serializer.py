from rest_framework import serializers


class GetLatestVideoSerializer(serializers.Serializer):
    count = serializers.IntegerField(required=False, default=3)


class GetVideosSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=True)


class AllMediaSerializer(serializers.Serializer):
    type = serializers.CharField(required=True, max_length=10)
    page = serializers.IntegerField(required=True)
    orderby = serializers.CharField(required=True, max_length=20)
    tags = serializers.ListField(required=False)
