import requests

from electric_meter.celery import app
from .models import ElectricMeter
from .serializers import DataSerializer


@app.task
def get_meter_data():
    meters = ElectricMeter.objects.all()
    for meter in meters:
#        response = requests.get(
#            'http://{}:{}'.format(meter.address, meter.port)
#        )
        response = requests.get(
            'http://{}:8001/{}'.format(meter.address, meter.port)
        )
        data = response.json()
        serializer = DataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
