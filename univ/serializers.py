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


class UnivRankingDetailSerializer(serializers.Serializer):
    project_count = serializers.IntegerField()
    completed_projects = serializers.IntegerField()
    project_score = serializers.FloatField()
    completion_score = serializers.FloatField()
    quality_score = serializers.FloatField()
    completed_ratio = serializers.FloatField()
    avg_features = serializers.FloatField()
    avg_tech_stacks = serializers.FloatField()


class UnivRankingSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    id = serializers.IntegerField()
    name = serializers.CharField()
    region = serializers.CharField()
    total_score = serializers.FloatField()
    details = UnivRankingDetailSerializer()


class UnivRankingResponseSerializer(serializers.Serializer):
    rankings = UnivRankingSerializer(many=True)
    total_count = serializers.IntegerField()
    performance = serializers.DictField(required=False)  # 성능 정보를 위한 선택적 필드
