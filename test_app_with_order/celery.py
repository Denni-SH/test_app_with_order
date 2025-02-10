import os
from celery import Celery, shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_app_with_order.settings')
app = Celery('test_app_with_order')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
