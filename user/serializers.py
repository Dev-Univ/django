from rest_framework import serializers


# 나중을 위해 일단 Request Response 나눠둠
class UserProfileRequestSerializer(serializers.Serializer):
    school = serializers.CharField(max_length=100)
    major = serializers.CharField(max_length=100)
    self_introduction = serializers.CharField(max_length=255)
    github_url = serializers.CharField(max_length=255)
    is_profile_private = serializers.BooleanField(default=False)


class UserProfileResponseSerializer(serializers.Serializer):
    school = serializers.CharField(max_length=100)
    major = serializers.CharField(max_length=100)
    self_introduction = serializers.CharField(max_length=255)
    github_url = serializers.CharField(max_length=255)
    is_profile_private = serializers.BooleanField(default=False)

