from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lecture_alert.settings')

app = Celery('lecture_alert')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule task to run every 5 minutes
app.conf.beat_schedule = {
    'check-upcoming-lectures': {
        'task': 'notification.tasks.check_and_send_notifications',
        'schedule': 300.0,  # 5 minutes
    }
}

app.conf.timezone = 'UTC'