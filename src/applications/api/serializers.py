from rest_framework import serializers


class ActiveConferenceSerializer(serializers.Serializer):
    short_name = serializers.CharField()
    name = serializers.CharField()
    start_date = serializers.DateField()
    duration = serializers.CharField()
    format = serializers.CharField()
    grade = serializers.CharField()
