from rest_framework import serializers

from commissions.models import Commission


class CommissionReadSerializer(serializers.ModelSerializer):

    sale = serializers.CharField(source='sale.id')
    rule = serializers.CharField(source='percentage.name')
    user = serializers.CharField(source='user.code')

    class Meta:
        model = Commission
        fields = ('id', 'sale', 'amount', 'rule', 'user')
