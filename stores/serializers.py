from rest_framework import serializers
from stores.models import Region, City, Store


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('code', 'name', 'manager')

class CitySerializer(serializers.ModelSerializer):
    region_info = RegionSerializer(read_only=True)
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), write_only=True)

    class Meta:
        model = City
        fields = ('code', 'name', 'manager', 'region', 'region_info')

class StoreSerializer(serializers.ModelSerializer):
    city_info = serializers.SerializerMethodField(read_only=True)
    region_info = serializers.SerializerMethodField(read_only=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), write_only=True)


    class Meta:
        model = Store
        fields = ('code', 'name', 'manager', 'city', 'city_info', 'region_info')

    def get_region_info(self, obj):
        desired_fields = ['code', 'name']
        region_serializer = RegionSerializer(obj.city.region, context={'region_fields': desired_fields})
        return region_serializer.data

    def get_city_info(self, obj):
        desired_fields = ['code', 'name']
        city_serializer = CitySerializer(obj.city, context={'city_fields': desired_fields})
        return city_serializer.data