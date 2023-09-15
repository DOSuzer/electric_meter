import requests

from django.conf import settings
from electric_meter.celery import app
from .models import ElectricMeter
from .serializers import DataSerializer


@app.task
def get_data(address, port):
    if settings.DEBUG:
        path = 'http://{}:8001/{}'.format(address, port)
    else:
        path = 'http://{}:{}'.format(address, port)
    try:
        response = requests.get(path)
    except Exception as e:
        print('Не удаслоь получить данные:', e)
    else:
        serializer = DataSerializer(data=response.json())
        serializer.is_valid(raise_exception=True)
        serializer.save()


@app.task
def get_meter_data():
    '''Фоновая задача собирающая данные с счетчиков.'''
    meters = ElectricMeter.objects.all()
    for meter in meters:
        get_data.delay(meter.address, meter.port)
