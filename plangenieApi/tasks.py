from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from .models import Schedule
from .utils.weather import fetch_weather
from .utils.notifications import get_device_token, send_push_notification


@shared_task
def send_weather(schedule_id: int):
    try:
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        return

    if schedule.weather_sent:
        return

    weather = fetch_weather(schedule.lat, schedule.lng)
    token = get_device_token(schedule.user_uuid)
    title = "Weather Alert"
    body = f"Weather code: {weather.get('weather_code')}"
    send_push_notification(token, title, body)

    schedule.weather_sent = True
    schedule.save(update_fields=["weather_sent"])


@shared_task
def schedule_weather(schedule_id: int):
    try:
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        return

    now = timezone.now()
    trigger_time = schedule.event_time - timedelta(hours=24)
    delay = (trigger_time - now).total_seconds()
    if delay <= 0:
        send_weather.delay(schedule_id)
    else:
        send_weather.apply_async((schedule_id,), countdown=delay)