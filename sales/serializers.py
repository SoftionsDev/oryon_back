import uuid

from products.models import Product
from products.serializers import ProductSerializer
from sales.models import Sale
from rest_framework import serializers

from stores.models import Store
from stores.serializers import StoreReadSerializer
from users.models import User
from users.serializers import UserSerializer
from utils.serializers import CustomDecimalField


class SaleReadSerializer(serializers.ModelSerializer):

    commercial = serializers.SerializerMethodField()
    store = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ('id', 'commercial', 'store', 'product', 'date', 'price')

    def get_commercial(self, obj):
        desired_fields = ['code', 'email']
        serializer = UserSerializer(obj.commercial, context={'fields': desired_fields})
        return serializer.data

    def get_store(self, obj):
        desired_fields = ['code', 'name']
        serializer = StoreReadSerializer(obj.store, context={'fields': desired_fields})
        return serializer.data

    def get_product(self, obj):
        desired_fields = ['code', 'name']
        serializer = ProductSerializer(obj.product, context={'fields': desired_fields})
        return serializer.data


class SalesWriteSerializer(serializers.Serializer):

    commercial_id = serializers.CharField(max_length=10)
    store_id = serializers.CharField(max_length=10)
    product_id = serializers.CharField(max_length=10)
    date = serializers.DateField(
        format="%Y-%m-%d", input_formats=['%d/%m/%Y', '%d-%m-%Y']
    )
    price = CustomDecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        if not data.get('id'):
            data['id'] = uuid.uuid4()

        data['commercial'] = User.objects.filter(code=data['commercial_id']).first()
        data['store'] = Store.objects.filter(code=data['store_id']).first()
        data['product'] = Product.objects.filter(code=data['product_id']).first()

        if not data['commercial']:
            raise serializers.ValidationError(f'User {data["commercial_id"]} does not exists')
        if not data['store']:
            raise serializers.ValidationError(f'Store {data["store_id"]} does not exists')
        if not data['product']:
            raise serializers.ValidationError(f'Product {data["product_id"]} does not exists')

        return data

    def create(self, validated_data):
        sale = Sale.objects.create(
            id=validated_data['id'],
            commercial=validated_data['commercial'],
            store=validated_data['store'],
            product=validated_data['product'],
            date=validated_data['date'],
            price=validated_data['price'],
        )
        return sale