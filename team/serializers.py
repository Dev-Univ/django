import json

from rest_framework import serializers


class PositionRequestSerializer(serializers.Serializer):
    role = serializers.CharField()
    max_members = serializers.IntegerField()
    current_members = serializers.IntegerField()
    description = serializers.CharField()
    is_open = serializers.BooleanField()


class TeamRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    theme_id = serializers.IntegerField(allow_null=True, required=False)
    type = serializers.CharField()
    period = serializers.CharField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    collaboration_method = serializers.CharField()
    end_date = serializers.DateField()
    tech_stacks = serializers.ListField(child=serializers.IntegerField(), required=False)
    positions = PositionRequestSerializer(many=True)


class PositionResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    role = serializers.CharField()
    max_members = serializers.IntegerField()
    current_members = serializers.IntegerField()
    description = serializers.CharField()
    is_open = serializers.BooleanField()


class TeamLeaderResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    school = serializers.CharField(source='profile.school')


class TeamTechStackResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='tech_stack.id')
    title = serializers.CharField(source='tech_stack.title')
    category = serializers.CharField(source='tech_stack.category')
    sub_category = serializers.CharField(source='tech_stack.sub_category')


class TeamResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    period = serializers.CharField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    collaboration_method = serializers.CharField()
    end_date = serializers.DateField()
    created_at = serializers.DateTimeField()
    positions = PositionResponseSerializer(many=True)
    tech_stacks = TeamTechStackResponseSerializer(many=True)
    user = TeamLeaderResponseSerializer()
