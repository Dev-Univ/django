from rest_framework import serializers


class ProjectFeatureRequestSerializer(serializers.Serializer):
    description = serializers.CharField()


class ProjectRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    is_done = serializers.BooleanField(default=False)
    short_description = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    main_image = serializers.ImageField()
    features = ProjectFeatureRequestSerializer(many=True, required=False, default=list)


class ProjectImageResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image_url = serializers.CharField(max_length=255)


class ProjectFeatureResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description = serializers.CharField()


class ProjectResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    is_done = serializers.BooleanField(default=False)
    short_description = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    main_image_url = serializers.CharField(max_length=255)
    additional_images = ProjectImageResponseSerializer(many=True)
    features = ProjectFeatureResponseSerializer(many=True)
