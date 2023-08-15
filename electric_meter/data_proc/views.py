import datetime
import requests

from django.conf import settings
from django.db.models import Avg, Max, Min
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MeterData, ElectricMeter
from .serializers import DataSerializer, MeterSerializer


class MeterViewSet(viewsets.ModelViewSet):
    '''Вьюсет получения данных, создания и удаления счетчиков.'''
    http_method_names = ['get', 'post', 'delete']
    queryset = ElectricMeter.objects.all()
    serializer_class = MeterSerializer

    @action(detail=True,
            methods=['get', ],
            url_path=r'data')
    def meter_data(self, request, pk):
        '''Получение данных с счетчика.'''
        meter = get_object_or_404(ElectricMeter, pk=self.kwargs.get('pk'))
        if settings.DEBUG:
            path = 'http://{}:8001/{}'.format(meter.address, meter.port)
        else:
            path = 'http://{}:{}'.format(meter.address, meter.port)
        try:
            response = requests.get(path)
        except Exception as e:
            return JsonResponse({'error': 'Не удаслоь получить данные!',
                                 'detail': str(e)})
        else:
            serializer = DataSerializer(data=response.json())
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['get', ],
            url_path=r'stats')
    def meter_stats(self, request, pk):
        '''Получение статистики по показаниям счетчика.'''
        meter_id = self.kwargs.get('pk')
        start_date = make_aware(datetime.datetime.strptime(
            request.data.get('start_date'), "%d-%m-%Y"
        ))
        end_date = make_aware(datetime.datetime.strptime(
            request.data.get('end_date'), "%d-%m-%Y"
        ))
        meter_data = (
            MeterData.objects
            .filter(meter_id=meter_id,
                    date__range=[start_date, end_date])
            .aggregate(avg_current=Avg('current'),
                       avg_consumption=Avg('consumption'),
                       total_consumption=Max('consumption')-Min('consumption'))
        )
        return JsonResponse(
            {'средний ток': meter_data['avg_current'],
             'среднее потребление': meter_data['avg_consumption'],
             'общее потребление': meter_data['total_consumption']}
        )
