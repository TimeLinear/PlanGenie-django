import os
from datetime import datetime
import requests

from django.conf import settings
from .grid import convert_to_grid
from datetime import datetime, date as date_type, time as time_type


def fetch_weather(
    lat: float,
    lon: float,
    date: date_type | None = None,
    time: time_type | None = None,
) -> dict:
    """Call the KMA API and return weather code and alert flag for the given coordinates and time."""

    service_key = settings.WEATHER_API_KEY
    nx, ny = convert_to_grid(lat, lon)

    # Default to current date if not provided
    if date is None:
        base_date = datetime.now().strftime("%Y%m%d")
    else:
        base_date = date.strftime("%Y%m%d")

    # `VilageFcst` requires a base time but we always request the 05:00 run
    base_time = "0500"

    # Forecast time to search for in the response
    if time is None:
        fcst_time = datetime.now().strftime("%H%M")
    else:
        fcst_time = time.strftime("%H%M")

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
        res.raise_for_status()
        items = res.json()["response"]["body"]["items"]["item"]
        pty_value = next(
            (
                i["fcstValue"]
                for i in items
                if i["category"] == "PTY"
                and i.get("fcstDate") == base_date
                and i.get("fcstTime") == fcst_time
            ),
            "0",
        )
        alert = pty_value in ["1", "2", "3"]
        return {"weather_code": pty_value, "alert": alert}
    except Exception:
        return {"error": "Failed to fetch weather info."}