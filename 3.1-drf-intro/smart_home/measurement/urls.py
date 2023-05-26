from django.urls import path
from .views import SensorViev, SensorDetailViev


urlpatterns = [
    path('sensors/', SensorViev.as_view()),
    path('sensors/<pk>/', SensorDetailViev.as_view()),
]
