from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from .serializers import ScheduleSerializer
from .models import Schedule
from .tasks import schedule_weather, send_weather

class ScheduleCreateAPIView(APIView):
    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        
        if serializer.is_valid():
            
            schedule = serializer.save()
            now = timezone.now()        
            if schedule.event_time - now <= timezone.timedelta(hours=24):
                send_weather.delay(schedule.id)
            else:
                schedule_weather.delay(schedule.id)
            return Response({"id": schedule.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
