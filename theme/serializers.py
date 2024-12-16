from rest_framework import serializers


class ThemeResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    # start_date < end_date validation 필요