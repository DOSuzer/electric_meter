import os

from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electric_meter.settings')

app = Celery('electric_meter')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# задача по сбору показаний с счетчиков
app.conf.beat_schedule = {
    'every': {
        'task': 'data_proc.tasks.get_meter_data',
        'schedule': int(settings.M,)
    },
}
