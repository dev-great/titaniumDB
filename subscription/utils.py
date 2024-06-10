
from django.utils import timezone


def default_expiration_date():
    return timezone.now() + timezone.timedelta(days=30)
