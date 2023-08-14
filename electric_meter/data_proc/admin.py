from django.contrib import admin

from .models import ElectricMeter, MeterData


@admin.register(ElectricMeter)
class ElectricMeterAdmin(admin.ModelAdmin):
    list_display = ('meter_id', 'address', 'port')
    empty_value_display = '-пусто-'


@admin.register(MeterData)
class MeterDataAdmin(admin.ModelAdmin):
    list_display = ('meter', 'current', 'consumption', 'date')
    empty_value_display = '-пусто-'
