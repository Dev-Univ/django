import json

from rest_framework import serializers


class ProjectMemberRequestSerializer(serializers.Serializer):
    role = serializers.CharField()
    user_email = serializers.EmailField()
    description = serializers.CharField()


class TimeLineRequestSerializer(serializers.Serializer):
    date = serializers.DateField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    order = serializers.IntegerField()


class ProjectRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    form_mode = serializers.CharField(default='BASIC_FORM')
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    status = serializers.CharField(max_length=100)
    short_description = serializers.CharField()
    description = serializers.CharField()
    main_image = serializers.ImageField()
    additional_images = serializers.ListField(child=serializers.ImageField(), max_length=5, required=False)
    features = serializers.ListField(child=serializers.CharField())
    tech_stacks = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    univ = serializers.ListField(child=serializers.IntegerField())
    members = serializers.JSONField()
    time_lines = serializers.JSONField()
    read_me_content = serializers.CharField()

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

    def validate_members(self, value):

        if isinstance(value, str):
            data = json.loads(value)
        else:
            data = value

        serializer = ProjectMemberRequestSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


class ProjectUserResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()


class ProjectImageResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image_url = serializers.CharField(max_length=255)


class ProjectFeatureResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField()


class ProjectTechStackResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='tech_stack.id')
    title = serializers.CharField(source='tech_stack.title')
    code = serializers.CharField(source='tech_stack.code')
    category = serializers.CharField(source='tech_stack.category')
    sub_category = serializers.CharField(source='tech_stack.sub_category')


class ProjectMemberResponseSerializer(serializers.Serializer):
    email = serializers.EmailField(source='user.email')
    name = serializers.CharField(source='user.name')
    school = serializers.CharField(source='user.profile.school')
    self_introduction = serializers.CharField(source='user.profile.self_introduction')
    github_url = serializers.CharField(source='user.profile.github_url')
    description = serializers.CharField()
    role = serializers.CharField()


class TimeLineResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    order = serializers.IntegerField()


class ProjectUnivResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='univ.id')
    name = serializers.CharField(source='univ.name')
    description = serializers.CharField(source='univ.description')
    region = serializers.CharField(source='univ.region')


class ProjectResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = ProjectUserResponseSerializer()
    title = serializers.CharField(max_length=100)
    form_mode = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    status = serializers.CharField(max_length=100)
    short_description = serializers.CharField()
    description = serializers.CharField()
    main_image_url = serializers.CharField(max_length=255)
    additional_images = ProjectImageResponseSerializer(many=True)
    features = ProjectFeatureResponseSerializer(many=True)
    tech_stacks = ProjectTechStackResponseSerializer(many=True)
    members = ProjectMemberResponseSerializer(many=True)
    project_univs = ProjectUnivResponseSerializer(many=True)
    time_lines = TimeLineResponseSerializer(many=True)
    is_owner = serializers.SerializerMethodField()
    read_me_content = serializers.CharField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return request.user.email == obj.user.email

