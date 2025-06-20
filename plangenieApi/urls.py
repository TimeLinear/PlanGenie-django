from django.urls import path
from .views import WeatherCheckAPIView

urlpatterns = [
    path('weather-check/', WeatherCheckAPIView.as_view(), name='weather-check'),
]
