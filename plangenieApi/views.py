from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import WeatherRequestSerializer
from .utils.weather import fetch_weather


class WeatherAPIView(APIView):

    def post(self, request):
        serializer = WeatherRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            weather = fetch_weather(
                data["lat"],
                data["lng"],
                data["date"],
                data["time"],
            )
            return Response(weather, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)