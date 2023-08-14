import datetime
import requests

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
    http_method_names = ['get', 'post', 'delete']
    queryset = ElectricMeter.objects.all()
    serializer_class = MeterSerializer

    @action(detail=True,
            methods=['get', ],
            url_path=r'data')
    def meter_data(self, request, pk):
        meter = get_object_or_404(ElectricMeter, pk=self.kwargs.get('pk'))
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
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['get', ],
            url_path=r'stats')
    def meter_stats(self, request, pk):
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
        print(meter_data)
        return JsonResponse(
            {'средний ток': meter_data['avg_current'],
             'среднее потребление': meter_data['avg_consumption'],
             'общее потребление': meter_data['total_consumption']}
        )
