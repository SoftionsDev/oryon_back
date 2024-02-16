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

    user = UserSerializer(context={'fields': ['code', 'email', 'first_name', 'last_name']})
    store = StoreReadSerializer(context={'fields': ['code', 'name']})
    product = ProductSerializer(context={'fields': ['code', 'name']})

    class Meta:
        model = Sale
        fields = (
            'id', 'user', 'store', 'product', 'date',
            'price', 'type', 'commission_type', 'commissioned'
        )


class SalesWriteSerializer(serializers.Serializer):

    user_id = serializers.CharField(max_length=10)
    store_id = serializers.CharField(max_length=10)
    product_id = serializers.CharField(max_length=10)
    date = serializers.DateField(
        format="%Y-%m-%d", input_formats=['%d/%m/%Y', '%d-%m-%Y']
    )
    price = CustomDecimalField(max_digits=10, decimal_places=2)
    type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    commission_type = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('id'):
            data['id'] = uuid.uuid4()

        data['user'] = User.objects.filter(code=data['user_id']).first()
        data['store'] = Store.objects.filter(code=data['store_id']).first()
        data['product'] = Product.objects.filter(code=data['product_id']).first()

        if not data['user']:
            raise serializers.ValidationError(f'User {data["user_id"]} does not exists')
        if not data['store']:
            raise serializers.ValidationError(f'Store {data["store_id"]} does not exists')
        if not data['product']:
            raise serializers.ValidationError(f'Product {data["product_id"]} does not exists')

        return data

    def create(self, validated_data):
        sale = Sale.objects.create(
            id=validated_data['id'],
            user=validated_data['user'],
            store=validated_data['store'],
            product=validated_data['product'],
            date=validated_data['date'],
            price=validated_data['price'],
            type=validated_data.get('type', None),
            commission_type=validated_data.get('commission_type', None)
        )
        return sale