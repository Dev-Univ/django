from rest_framework import serializers


class UnivResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    region = serializers.CharField(read_only=True)
    student_count = serializers.IntegerField(read_only=True)
    project_count = serializers.IntegerField(read_only=True)


class UnivInfoResponseSerializer(serializers.Serializer):
    class TotalStatsSerializer(serializers.Serializer):
        univs = serializers.IntegerField()
        projects = serializers.IntegerField()
        students = serializers.IntegerField()

    total_info = TotalStatsSerializer()
    universities = UnivResponseSerializer(many=True)
