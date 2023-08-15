from django.core.validators import MinValueValidator
from django.db import models


class ElectricMeter(models.Model):
    '''Модель счетчиков с id и адресом'''
    meter_id = models.CharField(max_length=50,
                                verbose_name='id счетчика',
                                unique=True,
                                primary_key=True)
    address = models.GenericIPAddressField(verbose_name='ip адрес счетчика', )
    port = models.PositiveIntegerField(verbose_name='порт счетчика',
                                       validators=[MinValueValidator(1), ])

    class Meta:
        ordering = ['-meter_id']
        verbose_name = 'Электросчетчик'
        verbose_name_plural = 'Электросчетчики'

    def __str__(self):
        return self.meter_id


class MeterData(models.Model):
    '''Модель данных с счетчиков'''
    meter = models.ForeignKey(
        ElectricMeter,
        on_delete=models.CASCADE,
        related_name='data',
    )
    current = models.FloatField(validators=[MinValueValidator(0), ])
    consumption = models.FloatField(validators=[MinValueValidator(0), ])
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Показания счетчика'
        verbose_name_plural = 'Показания счетчиков'

    def __str__(self):
        return f'{self.meter.meter_id}: {self.consumption}'
