import os
from datetime import datetime
import requests

from django.conf import settings
from .grid import convert_to_grid


def fetch_weather(lat: float, lon: float) -> dict:
    """Call the KMA API and return weather code and alert flag."""
    service_key = settings.WEATHER_API_KEY
    nx, ny = convert_to_grid(lat, lon)
    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    base_time = "0500"
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        "serviceKey": service_key,
        "pageNo": "1",
        "numOfRows": "1000",
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }
    try:
        res = requests.get(url, params=params)
        items = res.json()["response"]["body"]["items"]["item"]
        pty_value = next((i["fcstValue"] for i in items if i["category"] == "PTY"), "0")
        alert = pty_value in ["1", "2", "3"]
        return {"weather_code": pty_value, "alert": alert}
    except Exception:
        return {"error": "Failed to fetch weather info."}