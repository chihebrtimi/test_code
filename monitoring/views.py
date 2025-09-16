# monitoring/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate, get_user_model

from .models import SensorData, Message
from .serializers import SensorDataSerializer, UserSerializer, MessageSerializer

# ✅ Always resolve your active user model (CustomUser)
User = get_user_model()


# 🟢 Messages ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("-timestamp")
    serializer_class = MessageSerializer


# 🟢 SensorData ViewSet
class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all().order_by("-timestamp")
    serializer_class = SensorDataSerializer


# 🟢 Submit sensor data (public endpoint for STM32)
@api_view(["POST"])
def submit_sensor_data(request):
    serializer = SensorDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🟢 Login endpoint (for Flutter frontend)
@api_view(["POST"])
def login_user(request):
    email = request.data.get("email", "").lower()
    password = request.data.get("password", "")

    print("DEBUG: email =", email)
    print("DEBUG: password =", password)

    user = authenticate(request, email=email, password=password)
    print("DEBUG: user =", user)

    if user is not None:
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# 🟢 Admin: List users
@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# 🟢 Admin: Update user role
@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def update_user_role(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    is_staff = request.data.get("is_staff", None)
    if is_staff is not None:
        user.is_staff = is_staff
        user.save()

    serializer = UserSerializer(user)
    return Response(serializer.data)
