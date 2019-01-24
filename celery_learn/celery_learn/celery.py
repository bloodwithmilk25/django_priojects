import os
from celery import Celery
from celery.schedules import crontab

# https://code.tutsplus.com/ru/tutorials/using-celery-with-django-for-background-task-processing--cms-28732
# $ redis-server
# $ celery worker -A celery_learn --loglevel=debug --concurrency=4

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_learn.settings')

app = Celery('celery_learn')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'publish.tasks.send_view_count_report',
        'schedule': crontab(hour=20, minute=7),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}