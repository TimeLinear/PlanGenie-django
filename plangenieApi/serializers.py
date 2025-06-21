from rest_framework import serializers
from datetime import datetime
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    userUUID = serializers.CharField(source="user_uuid")
    localId = serializers.CharField(source="local_id")
    date = serializers.DateField(write_only=True)
    time = serializers.TimeField(write_only=True)
    lat = serializers.FloatField(source="lat")
    lng = serializers.FloatField(source="lng")

    class Meta:
        model = Schedule
        fields = [
            "id",
            "userUUID",
            "localId",
            "date",
            "time",
            "lat",
            "lng",
        ]

    def create(self, validated_data):
        date = validated_data.pop("date")
        time = validated_data.pop("time")
        event_time = datetime.combine(date, time)
        return Schedule.objects.create(event_time=event_time, **validated_data)


class WeatherRequestSerializer(serializers.Serializer):
    """Serializer for on-demand weather queries."""

    date = serializers.DateField()
    time = serializers.TimeField()
    lat = serializers.FloatField()
    lng = serializers.FloatField()