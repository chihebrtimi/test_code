# monitoring/serializers.py
# -------------------------
# This file defines the JSON shapes (serializers) your frontend consumes.
# Keep these stable: the UI should rely on these fields, not on DB internals.

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message
from .models import SensorData, LoginHistory

# Always resolve the active user model (your CustomUser) via get_user_model()
User = get_user_model()


# ╔══════════════════════════════════════════════════════════════════════╗
# ║ SensorData → read-only timestamp; expose all sensor numeric fields.  ║
# ╚══════════════════════════════════════════════════════════════════════╝
class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        # Be explicit for API contracts (clear & stable ordering)
        fields = [
            "id",
            "timestamp",
            "T_cold", "Humidity_cold",
            "T_hot_rack1", "Humidity_rack1",
            "T_hot_rack2", "Humidity_rack2",
            "T_hot_rack3", "Humidity_rack3",
            "T_room", "Room_Humidity",
            "P_total_room", "P_total_cooling_system",
            "P_rack1", "P_rack2",
        ]
        # Backend controls timestamp; client should not set it
        read_only_fields = ["id", "timestamp"]


# ╔══════════════════════════════════════════════════════════════════════╗
# ║ User (CustomUser) → expose safe account fields for the frontend.     ║
# ║ No password here. Email is your login identifier.                    ║
# ╚══════════════════════════════════════════════════════════════════════╝
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # resolves to monitoring.CustomUser
        fields = [
            "id",
            "email",
            "is_staff",
            "is_active",
            "is_superuser",   # read-only below; useful for UI visibility badges
            "last_login",
            "date_joined",
        ]
        # Protect critical/derived fields from being written via this serializer
        read_only_fields = ["id", "email", "is_superuser", "last_login", "date_joined"]


# ╔══════════════════════════════════════════════════════════════════════╗
# ║ LoginHistory → show who logged in, when, and from which IP.          ║
# ║ Includes a convenience read-only 'user_email' for the UI.            ║
# ╚══════════════════════════════════════════════════════════════════════╝
class LoginHistorySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = LoginHistory
        fields = ["id", "user", "user_email", "timestamp", "ip_address"]
        read_only_fields = ["id", "timestamp", "user_email"]
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"