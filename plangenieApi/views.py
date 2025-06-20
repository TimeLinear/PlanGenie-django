from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WeatherRequestSerializer
from .utils import convert_to_grid
import os, requests
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta

class WeatherCheckAPIView(APIView):
    def post(self, request):
        serializer = WeatherRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            
            service_key = os.getenv("KMA_API_KEY")  # 기상청 API KEY

            print("DEBUG: service_key =", service_key)

            lat = serializer.validated_data['latitude']
            lon = serializer.validated_data['longitude']

            nx, ny = convert_to_grid(lat, lon)

            # 2. 기준 날짜 및 시간 설정
            now = datetime.now()
            base_date = now.strftime("%Y%m%d")
            base_time = "0500"  # 새벽 5시 기준 데이터가 제일 안정적

            # 3. API 요청
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
                items = res.json()['response']['body']['items']['item']
                pty_value = next((i['fcstValue'] for i in items if i['category'] == 'PTY'), "0")

                # PTY(강수형태): 0 없음, 1 비, 2 비/눈, 3 눈
                alert = pty_value in ["1", "2", "3"]

                return Response({
                    "weather_code": pty_value,
                    "alert": alert
                })
            except Exception:
                return Response({"error": "Failed to fetch weather info."}, status=500)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
