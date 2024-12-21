import json

from rest_framework import serializers


class PositionRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
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
    name = serializers.CharField()
    description = serializers.CharField()
    is_open = serializers.BooleanField()


class TeamResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    description = serializers.CharField()
    end_date = serializers.DateField()
    positions = PositionResponseSerializer(many=True)