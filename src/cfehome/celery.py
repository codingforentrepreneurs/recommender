import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')

app = Celery('cfehome')

# CELERY_
app.config_from_object("django.conf:settings", namespace='CELERY')

# app.conf.broker_url = ''
# app.conf.result_backend ='django-db'
app.autodiscover_tasks()