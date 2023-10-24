from rest_framework import viewsets

from stores.models import Store, Region, City
from stores.serializers import StoreSerializer, RegionSerializer, CitySerializer
from utils.permissions import IsManager


class RegionalViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.select_related('city', 'city__region').all()
    serializer_class = StoreSerializer

    #def get_permissions(self):
    #    if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #        permission_classes = [IsManager]
    #    else:
    #        permission_classes = []
    #    return [permission() for permission in permission_classes]
