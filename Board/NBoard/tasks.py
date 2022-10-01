from datetime import timedelta, datetime
from celery import shared_task
from .models import OneTimeCode


@shared_task
def delete_old_codes():
    old_codes = OneTimeCode.objects.all().exclude(creation__gt=datetime.now() - timedelta(minutes=1))
    old_codes.delete()
