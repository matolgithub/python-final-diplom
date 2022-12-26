import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders.settings')

from django.conf import settings

app = Celery('orders')

app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
