from rest_framework import serializers


class ProjectFeatureRequestSerializer(serializers.Serializer):
    description = serializers.CharField()


class ProjectTechStackRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ProjectRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    is_done = serializers.BooleanField(default=False)
    short_description = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    main_image = serializers.ImageField()
    features = serializers.ListField(child=serializers.CharField())
    tech_stacks = serializers.ListField(child=serializers.IntegerField())
    members = serializers.ListField(child=serializers.EmailField())


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


class ProjectResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    is_done = serializers.BooleanField(default=False)
    short_description = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    main_image_url = serializers.CharField(max_length=255)
    additional_images = ProjectImageResponseSerializer(many=True)
    features = ProjectFeatureResponseSerializer(many=True)
    tech_stacks = ProjectTechStackResponseSerializer(source='tech_stacks.all', many=True)
    members = ProjectMemberResponseSerializer(source='members.all', many=True)

