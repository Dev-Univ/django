from rest_framework import serializers

from user.models import User


class NoticeResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    category = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    is_pinned = serializers.BooleanField()
    is_active = serializers.BooleanField()
    author = serializers.CharField(source='author.name')
