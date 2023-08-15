from rest_framework import serializers

from .models import ElectricMeter, MeterData


class DataSerializer(serializers.ModelSerializer):
    '''Сериализатор показаний с счетчика.'''
    id = serializers.PrimaryKeyRelatedField(
        source='meter',
        queryset=ElectricMeter.objects.all()
    )
    A = serializers.FloatField(source='current')
    kW = serializers.FloatField(source='consumption')

    class Meta:
        fields = ('id', 'A', 'kW')
        model = MeterData

    def validate_id(self, value):
        if not ElectricMeter.objects.filter(meter_id=value).exists():
            raise serializers.ValidationError('Неверный id счетчика!')
        return value

    def validate_A(self, value):
        if value < 0:
            raise serializers.ValidationError('Неверные данные!')
        return value

    def validate_kW(self, value):
        if value < 0:
            raise serializers.ValidationError('Неверные данные!')
        return value


class MeterSerializer(serializers.ModelSerializer):
    '''Сериализатор счетчика.'''
    class Meta:
        fields = ('meter_id', 'address', 'port')
        model = ElectricMeter
