from django.urls import include, path
from rest_framework import routers

from .views import MeterViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('meters', MeterViewSet, basename='meters')

urlpatterns = [
    path('', include(router_v1.urls)),
]
