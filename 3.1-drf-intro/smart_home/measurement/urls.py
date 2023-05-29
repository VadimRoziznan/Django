from django.urls import path
from .views import SensorView, SensorDetailViev


urlpatterns = [
    path('sensors/', SensorView.as_view()),
    path('sensors/<pk>/', SensorView.as_view()),
    path('measurements', SensorDetailViev.as_view()),
]
