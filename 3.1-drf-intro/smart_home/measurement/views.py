# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    RetrieveUpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Sensor, Measurement
from .serializers import SensorDetailSerializer, MeasurementSerializer



class SensorViev(ListAPIView):

    def get(self, request):
        sensor = Sensor.objects.all()
        ser = SensorDetailSerializer(sensor, many=True)
        return Response(ser.data)


class SensorDetailViev(RetrieveAPIView):

    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


