from rest_framework import serializers

from products.models import Product
from utils.serializers import SelectableFieldsModelSerializer


class ProductSerializer(SelectableFieldsModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'