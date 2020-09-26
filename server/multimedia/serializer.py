from rest_framework import serializers


class GetLatestVideoSerializer(serializers.Serializer):
    count = serializers.IntegerField(required=False, default=3)
