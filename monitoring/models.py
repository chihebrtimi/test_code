# monitoring/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission


# 🔑 Custom Manager (email login)
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


# 🔑 Custom User with email only
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    groups = None  # 🚫 Remove Groups
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="customuser_set",
        related_query_name="customuser",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# 🌡 Sensor Data (structured measurements)
class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    T_cold = models.FloatField()
    Humidity_cold = models.FloatField()
    T_hot_rack1 = models.FloatField()
    Humidity_rack1 = models.FloatField()
    T_hot_rack2 = models.FloatField()
    Humidity_rack2 = models.FloatField()
    T_hot_rack3 = models.FloatField()
    Humidity_rack3 = models.FloatField()
    T_room = models.FloatField()
    Room_Humidity = models.FloatField()
    P_total_room = models.FloatField()
    P_total_cooling_system = models.FloatField()
    P_rack1 = models.FloatField()
    P_rack2 = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} | Room Temp: {self.T_room}°C"


# 📩 Unified Message Table (for alerts/system logs)
class Message(models.Model):
    MESSAGE_TYPES = [
        ("sensor", "Sensor Data"),
        ("alert", "Alert"),
        ("system", "System Log"),
    ]

    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    content = models.TextField()
    data = models.JSONField(blank=True, null=True)
    source = models.CharField(max_length=100, default="STM32")

    def __str__(self):
        return f"[{self.type.upper()}] {self.timestamp} - {self.content[:50]}"


# 📜 Login History
class LoginHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} | {self.timestamp} | {self.ip_address or 'N/A'}"
