from rest_framework import serializers
from stores.models import Region, City, Store
from users.serializers import UserSerializer
from utils.serializers import SelectableFieldsModelSerializer


class RegionSerializer(SelectableFieldsModelSerializer):
    class Meta:
        model = Region
        fields = ('code', 'name', 'manager')

class CitySerializer(SelectableFieldsModelSerializer):
    region_info = RegionSerializer(read_only=True)
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), write_only=True)

    class Meta:
        model = City
        fields = ('code', 'name', 'manager', 'region', 'region_info')

class StoreSerializer(SelectableFieldsModelSerializer):
    city_info = serializers.SerializerMethodField(read_only=True)
    region_info = serializers.SerializerMethodField(read_only=True)
    manager_info = serializers.SerializerMethodField(read_only=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), write_only=True)

    class Meta:
        model = Store
        fields = ('code', 'name', 'manager', 'city', 'city_info', 'region_info', 'manager_info')

    def get_region_info(self, obj):
        desired_fields = ['code', 'name']
        serializer = RegionSerializer(obj.city.region, context={'fields': desired_fields})
        return serializer.data

    def get_city_info(self, obj):
        desired_fields = ['code', 'name']
        serializer = CitySerializer(obj.city, context={'fields': desired_fields})
        return serializer.data

    def get_manager_info(self, obj):
        desired_fields = ['code', 'email']
        serializer = UserSerializer(obj.manager, context={'fields': desired_fields})
        return serializer.data