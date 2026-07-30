import uuid
from datetime import timedelta
from django.utils import timezone


def generate_qr_token():
    return str(uuid.uuid4())


def get_expiry_time():
    return timezone.now() + timedelta(minutes=2)