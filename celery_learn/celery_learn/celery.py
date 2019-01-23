import os
from celery import Celery

# https://code.tutsplus.com/ru/tutorials/using-celery-with-django-for-background-task-processing--cms-28732

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_learn.settings')

app = Celery('celery_learn')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()