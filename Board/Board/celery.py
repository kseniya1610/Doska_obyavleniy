import os
from celery import Celery
from celery.schedules import crontab

"""
redis-server
celery -A Board worker -l INFO
celery -A Board beat -l INFO
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Board.settings')

app = Celery('Board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'every minute': {
        'task': 'NBoard.tasks.delete_old_codes',
        'schedule': crontab(),
    }
}

app.autodiscover_tasks()