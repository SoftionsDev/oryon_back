from rest_framework import serializers
from stores.models import Region, City, Store
from users.models import User
from users.serializers import UserSerializer
from utils.serializers import SelectableFieldsModelSerializer


class RegionReadSerializer(SelectableFieldsModelSerializer):

    manager = UserSerializer(read_only=True, context={'fields': ['code', 'email']})

    class Meta:
        model = Region
        fields = ('code', 'name', 'manager')


class RegionWriteSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)
    manager = serializers.SlugRelatedField(
        queryset=User.objects.filter(groups__name__in=['manager', 'admin']),
        slug_field='code',
        write_only=True
    )

    def create(self, validated_data):
        return Region.objects.create(**validated_data)


class CityReadSerializer(SelectableFieldsModelSerializer):
    region = RegionReadSerializer(read_only=True, context={'fields': ['code', 'name']})
    manager = UserSerializer(read_only=True, context={'fields': ['code', 'email']})

    class Meta:
        model = City
        fields = ('code', 'name', 'manager', 'region')


class CityWriteSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)
    manager = serializers.SlugRelatedField(
        queryset=User.objects.filter(groups__name__in=['manager', 'admin']),
        slug_field='code',
        write_only=True
    )
    region = serializers.SlugRelatedField(
        queryset=Region.objects.all(),
        slug_field='code',
        write_only=True
    )

    def create(self, validated_data):
        return City.objects.create(**validated_data)


class StoreReadSerializer(SelectableFieldsModelSerializer):

    manager = UserSerializer(read_only=True, context={'fields': ['code', 'email']})
    city = CityReadSerializer(read_only=True, context={'fields': ['code', 'name']})

    class Meta:
        model = Store
        fields = ('code', 'name', 'manager', 'city')


class StoreWriteSerializer(serializers.Serializer):

    code = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)
    manager = serializers.SlugRelatedField(
        queryset=User.objects.filter(groups__name__in=['manager', 'admin']),
        slug_field='code',
        write_only=True
    )
    city = serializers.SlugRelatedField(
        queryset=City.objects.all(),
        slug_field='code',
        write_only=True
    )

    def create(self, validated_data):
        try:
            store = Store.objects.create(**validated_data)
            return store
        except Exception as e:
            raise serializers.ValidationError(str(e))