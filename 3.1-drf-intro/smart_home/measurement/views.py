# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    RetrieveUpdateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Sensor, Measurement
from .serializers import SensorDetailSerializer, SensorSerializer


class SensorView(ListCreateAPIView, RetrieveUpdateAPIView):



    def get(self, request, *args, **kwargs):
        sensor = Sensor.objects.all()
        ser = SensorSerializer(sensor, many=True)
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        try:
            new_sensor = Sensor.objects.create(
                name=request.data.get('name'),
                description=request.data.get('description')
            )
            new_sensor.save()
        except Exception as error:
            return Response({'status': 'error', 'ERROR': str(error)})
        return Response({'status': 'OK'})

    def patch(self, request, *args, **kwargs):
        try:
            Sensor.objects.filter(pk=kwargs['pk']).update(
                description=request.data.get('description')
            )
        except Exception as error:
            return Response({'status': 'error', 'ERROR': str(error)})
        return Response({'status': 'OK'})




class SensorDetailViev(RetrieveAPIView, RetrieveUpdateAPIView):

        queryset = Sensor.objects.all()
        serializer_class = SensorDetailSerializer



