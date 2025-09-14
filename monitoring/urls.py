# monitoring/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorDataViewSet, submit_sensor_data, MessageViewSet

router = DefaultRouter()
router.register(r"sensordata", SensorDataViewSet, basename="sensordata")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
    path("submit/", submit_sensor_data),
]
