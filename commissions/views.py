import uuid

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from brm.models import Percentages
from brm.services import data_lookup, RulesExecutor
from commissions.models import Commission
from commissions.serializer import CommissionReadSerializer
from sales.models import Sale
from utils.permissions import IsAdmin, IsManager


class CommissionViews(ViewSet):

    permission_classes = [IsAdmin | IsManager]

    def list(self, request):
        commissions = Commission.objects.all()
        serializer = CommissionReadSerializer(commissions, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, name='generate')
    def generate(self, request):
        rules_handler = RulesExecutor(data_lookup)
        result = {'commissions': []}
        percentages = Percentages.objects.filter(
            is_active=True
        ).order_by('-created_at').select_related('formula')
        for sale in Sale.objects.filter(commissioned=False).iterator():
            for percentage in percentages:
                commission = rules_handler.execute(percentage, sale)
                if not commission:
                    continue
                Commission.objects.create(
                    id=uuid.uuid4(),
                    sale=sale,
                    amount=commission,
                    percentage=percentage,
                    user=sale.user
                )
                sale.commissioned = True
                sale.save()

                result['commissions'].append({
                    'sales_id': str(sale.id),
                    'commission': sale.commissioned,
                    'amount': commission
                })
                break

        return Response(result, status=status.HTTP_200_OK)

