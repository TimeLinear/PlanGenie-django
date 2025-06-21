from django.db import models

class Schedule(models.Model):
    user_uuid = models.CharField(max_length=64)
    local_id = models.CharField(max_length=128)
    event_time = models.DateTimeField()
    lat = models.FloatField()
    lng = models.FloatField()
    weather_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_uuid} - {self.local_id}"