import random

from django.core.management.base import BaseCommand

from ...models import ElectricMeter, MeterData


class Command(BaseCommand):
    help = 'Заполнение базы данными с счетчика 1000'

    def handle(self, *args, **kwargs):
        '''В данном случае id счетчика совпадает с портом для упрощения.'''
        kW = 50
        meter = ElectricMeter.objects.get(meter_id='1000')
        for i in range(0, 100):
            MeterData.objects.create(
                meter=meter,
                current=random.randint(0, 50),
                consumption=kW
            )
            kW += random.randint(0, 50)
        print('done!')
