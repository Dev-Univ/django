import json

from rest_framework import serializers


class PositionRequestSerializer(serializers.Serializer):
    role = serializers.CharField()
    quota = serializers.IntegerField()
    description = serializers.CharField()
    is_open = serializers.BooleanField()


class TeamRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    description = serializers.CharField()
    end_date = serializers.DateField()
    tech_stacks = serializers.ListField(child=serializers.IntegerField(), required=False)
    positions = PositionRequestSerializer(many=True)


class PositionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    role = serializers.CharField()
    quota = serializers.IntegerField()
    description = serializers.CharField()
    is_open = serializers.BooleanField()


class TeamLeaderResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    school = serializers.CharField(source='profile.school')


class TeamResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    description = serializers.CharField()
    end_date = serializers.DateField()
    positions = PositionResponseSerializer(many=True)
    user = TeamLeaderResponseSerializer()
