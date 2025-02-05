import uuid

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class UserResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    profile_image_url = serializers.CharField()
    school = serializers.CharField(source='user_profile.school')
    major = serializers.CharField(source='user_profile.major')


class UserProfileTechStackRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class UserProfileRequestSerializer(serializers.Serializer):
    school = serializers.CharField(max_length=100, required=False, allow_blank=True)
    major = serializers.CharField(max_length=100, required=False, allow_blank=True)
    self_introduction = serializers.CharField(max_length=1000)
    github_url = serializers.CharField(max_length=255, required=False, allow_blank=True)
    is_profile_private = serializers.BooleanField(default=False)
    tech_stacks = serializers.ListField(child=serializers.CharField(required=False))


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    school = serializers.CharField(source='profile.school')
    major = serializers.CharField(source='profile.major')
    self_introduction = serializers.CharField(source='profile.self_introduction', max_length=255)


class UserProfileTechStackResponseSerializer(serializers.Serializer):
    title = serializers.CharField(source='tech_stack.title')
    code = serializers.CharField(source='tech_stack.code')
    category = serializers.CharField(source='tech_stack.category')
    sub_category = serializers.CharField(source='tech_stack.sub_category')


class PublicUserProfileResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    profile_image_url = serializers.CharField()
    school_email_verified = serializers.BooleanField()
    school = serializers.CharField(max_length=100, source='profile.school')
    major = serializers.CharField(max_length=100, source='profile.major')
    self_introduction = serializers.CharField(max_length=255, source='profile.self_introduction')
    github_url = serializers.CharField(max_length=255, source='profile.github_url')
    tech_stacks = UserProfileTechStackResponseSerializer(source='tech_stacks.all', many=True)


class PrivateUserProfileResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    profile_image_url = serializers.CharField()
    school_email_verified = serializers.BooleanField()
    school = serializers.CharField(max_length=100, source='profile.school')
    major = serializers.CharField(max_length=100, source='profile.major')
    self_introduction = serializers.CharField(max_length=1000, source='profile.self_introduction')
    github_url = serializers.CharField(max_length=255, source='profile.github_url')
    tech_stacks = UserProfileTechStackResponseSerializer(source='tech_stacks.all', many=True)
    is_profile_private = serializers.BooleanField(source='profile.is_profile_private')
    is_my_profile = serializers.BooleanField(default=True)

