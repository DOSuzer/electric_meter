from django.core.management.base import BaseCommand

from ...models import ElectricMeter


class Command(BaseCommand):
    help = 'Заполнение базы счетчиками'

    def handle(self, *args, **kwargs):
        '''В данном случае id счетчика совпадает с портом для упрощения.'''
        for i in range(1000, 1150):
            _, created = ElectricMeter.objects.get_or_create(
                meter_id=i,
                address='127.0.0.1',
                port=i
            )
        print('done!')
