# server_project/urls.py
from django.urls import path, include 
from django.http import JsonResponse 
from django.contrib.auth import views as auth_views 
from rest_framework.routers import DefaultRouter 
from monitoring.admin import custom_admin_site

from monitoring.views import (
    list_users,
    update_user_role,
    login_user,
    SensorDataViewSet,
    submit_sensor_data,
    MessageViewSet,
)

# Optional: Root index view
def index(request):
    return JsonResponse({"message": "Welcome to Server Monitoring API"})

# API router (SensorData + Messages)
router = DefaultRouter() 
router.register(r'sensordata', SensorDataViewSet) 
urlpatterns = [
    path('', index),

    # 🟢 Admin site
    path('admin/', custom_admin_site.urls ),  # if you’re using custom_admin_site, swap it here

    # 🟢 Sensor data + messages API
    path('submit/', submit_sensor_data),
    path('api/', include(router.urls)),   # /sensordata/ and /messages/

    # 🟢 Authentication
    path('api/login/', login_user),

    # 🟢 Admin users API
    path('api/users/', list_users),
    path('api/users/<int:user_id>/', update_user_role),
    # 🟢 Password reset (optional; uses Django auth views/templates) 
    path('api/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('api/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('api/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]
