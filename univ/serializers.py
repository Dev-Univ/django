from rest_framework import serializers


class UnivResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    region = serializers.CharField(read_only=True)
