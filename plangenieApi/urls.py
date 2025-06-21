from django.urls import path
from .views import ScheduleCreateAPIView

urlpatterns = [
    path('schedules/', ScheduleCreateAPIView.as_view(), name='schedule-create'),
]
