import json

from rest_framework import serializers


class ProjectFeatureRequestSerializer(serializers.Serializer):
    description = serializers.CharField()


class ProjectTechStackRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class TimeLineRequestSerializer(serializers.Serializer):
    date = serializers.DateField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()


class ProjectRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    is_done = serializers.BooleanField(default=False)
    short_description = serializers.CharField()
    description = serializers.CharField()
    main_image = serializers.ImageField()
    features = serializers.ListField(child=serializers.CharField())
    tech_stacks = serializers.ListField(child=serializers.IntegerField())
    members = serializers.ListField(child=serializers.EmailField())
    time_lines = serializers.JSONField()  # JSONField로 변경

    # 어쩔 수 없이 JSON 문자열을 파싱하고 TimeLineRequestSerializer로 검증
    # todo: 어떻게든 이거 바꾸고싶은데..
    def validate_time_lines(self, value):

        if isinstance(value, str):
            data = json.loads(value)
        else:
            data = value

        serializer = TimeLineRequestSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


class ProjectImageResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image_url = serializers.CharField(max_length=255)


class ProjectFeatureResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField()


class ProjectTechStackResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='tech_stack.id')
    title = serializers.CharField(source='tech_stack.title')
    category = serializers.CharField(source='tech_stack.category')
    sub_category = serializers.CharField(source='tech_stack.sub_category')


class ProjectMemberResponseSerializer(serializers.Serializer):
    email = serializers.EmailField(source='user.email')
    name = serializers.CharField(source='user.name')
    school = serializers.CharField(source='user.profile.school')
    self_introduction = serializers.CharField(source='user.profile.self_introduction')
    github_url = serializers.CharField(source='user.profile.github_url')
    role = serializers.CharField()


class TimeLineResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()


class ProjectResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    is_done = serializers.BooleanField(default=False)
    short_description = serializers.CharField()
    description = serializers.CharField()
    main_image_url = serializers.CharField(max_length=255)
    additional_images = ProjectImageResponseSerializer(many=True)
    features = ProjectFeatureResponseSerializer(many=True)
    tech_stacks = ProjectTechStackResponseSerializer(source='tech_stacks.all', many=True)
    members = ProjectMemberResponseSerializer(source='members.all', many=True)
    time_lines = TimeLineResponseSerializer(source='time_lines.all', many=True)

