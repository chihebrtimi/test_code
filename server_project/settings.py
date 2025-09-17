# server_project/settings.py
"""
API Contract: Settings (what the frontend should rely on)

- AUTH_USER_MODEL = 'monitoring.CustomUser'  → email-only login.
- REST API served by Django REST Framework (no browsable API assumptions required).
- Static assets served under STATIC_URL; custom admin CSS lives in /static/css/custom_admin.css.
- Admin UI available at /admin/ (custom admin site wired in project urls).

Security note:
- Keep SECRET_KEY and email credentials out of source control in production.
"""

from pathlib import Path
import socket
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True

# ✅ Dynamically detect LAN IP and add it to ALLOWED_HOSTS
def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

local_ip = get_lan_ip()

ALLOWED_HOSTS = ["127.0.0.1", "localhost", local_ip]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'monitoring',
    "corsheaders",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",   
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'server_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # custom admin & auth templates (e.g., base_site.html, login.html)
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server_project.wsgi.application'



AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static files setup
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",   # where your custom CSS (custom_admin.css) is
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # where collectstatic will copy everything

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ Email configuration for password reset (use app password in production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'server.room.access@gmail.com'
EMAIL_HOST_PASSWORD = 'vota vwfr ihgv uxwo'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ✅ Use custom user model (email-only)
AUTH_USER_MODEL = 'monitoring.CustomUser'
CORS_ALLOWED_ORIGINS = [
    "http://localhost:56574",   # replace with the exact URL Flutter web runs on
    "http://127.0.0.1:63465",
]
