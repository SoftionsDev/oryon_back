from rest_framework import viewsets

from stores.models import Store, Region, City
from stores import serializers
from utils.permissions import IsManager, IsAdmin


class BaseView(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin|IsManager]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class RegionalViewSet(BaseView):
    queryset = Region.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers.RegionWriteSerializer
        return serializers.RegionReadSerializer


class CityViewSet(BaseView):
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers.CityWriteSerializer
        return serializers.CityReadSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.select_related('city', 'city__region').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers.StoreWriteSerializer
        return serializers.StoreReadSerializer
