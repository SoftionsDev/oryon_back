from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from brm.models import Rule
from brm.services import data_lookup, RuleExecutor
from sales.models import Sale
from utils.permissions import IsAdmin, IsManager


class CommissionViews(ViewSet):

    permission_classes = [IsAdmin | IsManager]

    @action(methods=['POST'], detail=False, name='generate')
    def generate(self, request):
        rule_executor = RuleExecutor(data_lookup)
        result = {'rules_report': []}
        rules = Rule.objects.all().iterator()
        for sale in Sale.objects.filter(commissioned=False).iterator():
            for rule in rules:
                result['rules_report'].append({
                    'sales_id': str(sale.id),
                    'rule_id': str(rule.id),
                    'valid': rule_executor.execute_rule(rule.expression, sale)
                })

        return Response(result, status=status.HTTP_200_OK)

