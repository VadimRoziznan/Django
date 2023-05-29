from django.urls import path
from .views import SensorView, MeasurementView, SensorRetrieveView


urlpatterns = [
    path('sensors/', SensorView.as_view()),
    path('sensors/<pk>/', SensorRetrieveView.as_view()),
    path('measurements/', MeasurementView.as_view()),
]
