from rest_framework import serializers

from commissions.models import Commission
from users.serializers import UserSerializer


class CommissionReadSerializer(serializers.ModelSerializer):

    sale = serializers.CharField(source='sale.id')
    rule = serializers.CharField(source='percentage.name')
    user = UserSerializer()

    class Meta:
        model = Commission
        fields = ('id', 'sale', 'amount', 'rule', 'user')
