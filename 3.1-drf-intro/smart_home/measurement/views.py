from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Sensor, Measurement
from .serializers import SensorDetailSerializer, SensorSerializer
from datetime import datetime


class SensorRetrieveView(
    RetrieveAPIView, RetrieveUpdateAPIView
):
    """
    Implemented get method (gets values from the database and all related
    fields) and patch method (changes the value in the database).
    """

    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    def patch(self, request, *args, **kwargs):
        try:
            Sensor.objects.filter(pk=kwargs['pk']).update(
                description=request.data.get('description')
            )
        except Exception as error:
            return Response({'status': 'error', 'ERROR': str(error)})
        return Response({'status': 'OK'})


class SensorView(ListAPIView, ListCreateAPIView):
    """
    Implemented get method (gets all values from the database)
    and post method (creates a new value in the database).
    """

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


class MeasurementView(ListCreateAPIView):
    """
    Implemented post method (creates a new value in the database).
     """

    def post(self, request, *args, **kwargs):
        try:
            new_measurement = Measurement.objects.create(
                id_sensor_id=request.data.get('sensor'),
                temperature=request.data.get('temperature'),
                created_at=datetime.now()
            )
            new_measurement.save()
        except Exception as error:
            print(error)
            return Response({'status': 'error', 'ERROR': str(error)})
        return Response({'status': 'OK'})
