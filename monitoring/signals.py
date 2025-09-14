# monitoring/signals.py
"""
API Contract: Audit logging (implicit side-effect)

On successful user login (django.contrib.auth.signals.user_logged_in),
we create a LoginHistory row with:
- user: the authenticated CustomUser
- timestamp: auto (when saved)
- ip_address: derived from request headers (X-Forwarded-For -> Remote-Addr)

The frontend can read this via an admin API (if you expose one) or via Django admin.
"""

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import LoginHistory


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    LoginHistory.objects.create(user=user, ip_address=ip)


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0]
    return request.META.get('REMOTE_ADDR')
