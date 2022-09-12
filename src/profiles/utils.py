import datetime
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone


User = get_user_model()


def get_recent_users(days_ago=7, ids_only=True):
    delta = datetime.timedelta(days=days_ago)
    time_delta = timezone.now()  - delta
    qs = User.objects.filter(
        Q(date_joined__gte=time_delta) |
        Q(last_login__gte=time_delta) 
    )
    if ids_only:
        return qs.values_list('id', flat=True)
    return qs