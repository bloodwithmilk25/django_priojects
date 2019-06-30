import os
from celery import Celery
from django.conf import settings

# https://code.tutsplus.com/ru/tutorials/using-celery-with-django-for-background-task-processing--cms-28732
# $ redis-server
# MAC $ celery worker -A celery_learn --loglevel=debug --concurrency=4
# WINDOWS celery worker -A celery_learn --loglevel=debug --concurrency=4

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_learn.settings')

app = Celery('celery_learn')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')
