# server_project/urls.py
"""
API Contract: Project URL mounting

Public/Device:
- POST /submit/                      -> submit sensor row (same payload as SensorDataSerializer)

Auth:
- POST /api/login/                   -> email/password login (CustomUser)

Sensor Data (DRF router):
- GET  /api/sensordata/              -> list (ordered -timestamp)
- POST /api/sensordata/              -> create
- GET  /api/sensordata/<id>/         -> retrieve
- PUT/PATCH /api/sensordata/<id>/    -> update
- DELETE /api/sensordata/<id>/       -> delete

Admin-only:
- GET  /api/users/                   -> list users
- PATCH /api/users/<id>/             -> update user role (is_staff)

Admin UI:
- /admin/                            -> custom admin site (Monitoring Administration)
"""

from django.urls import path, include
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

from monitoring.views import (
    list_users,
    update_user_role,
    login_user,
    SensorDataViewSet,
    submit_sensor_data,
)

# 🔴 Import your custom admin site
from monitoring.admin import custom_admin_site


# Optional: Root index view
def index(request):
    return JsonResponse({"message": "Welcome to Server Monitoring API"})


# API router
router = DefaultRouter()
router.register(r'sensordata', SensorDataViewSet)

urlpatterns = [
    path('', index),

    # ✅ Use custom admin site instead of default
    path('admin/', custom_admin_site.urls),

    # 🟢 Sensor data API
    path('submit/', submit_sensor_data),
    path('api/', include(router.urls)),

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
