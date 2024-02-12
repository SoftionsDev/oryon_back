import calendar
from datetime import datetime
from decimal import Decimal

from django.db.models import Sum, Count, Prefetch, Value, Q
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from commissions.models import Commission
from users.serializers import UserSerializer, TokenSerializer, CommercialSerializer, UserCommissionSerializer
from utils.permissions import IsAdmin, IsManager
from users.models import User, Commercial


class UserViewSet(ModelViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('groups').all()
    permission_classes = [IsAdmin | IsManager]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.code == request.user.code:
            raise ValidationError('Cannot delete itself')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserToken(TokenObtainPairView):
    serializer_class = TokenSerializer


class CommercialViewSet(ModelViewSet):
    model = Commercial
    serializer_class = CommercialSerializer
    queryset = Commercial.objects.select_related('user', 'manager').all()
    permission_classes = [IsAdmin | IsManager]
    lookup_field = 'user__email'

    def get_queryset(self):
        if self.request.user.is_admin:
            return Commercial.objects.select_related(
                'user', 'manager'
            ).all()

        # it has to be a manager to retrieve other commercials
        manager_id = self.request.user.code
        return Commercial.objects.filter(
            manager_id=manager_id
        ).select_related('user', 'manager')

    @action(methods=['GET'], detail=True, name='commissions')
    def commissions(self, request, code=None):
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        _today = datetime.today()
        first_day_month = datetime(_today.year, _today.month, 1)
        _, _last_day_month = calendar.monthrange(_today.year, _today.month)
        last_day_month = datetime(_today.year, _today.month, _last_day_month)
        user_commissions = User.objects.filter(code=code).annotate(
            total_amount=Coalesce(
                Sum(
                    'commissions__amount',
                    filter=Q(
                        commissions__sale__date__range=(
                            first_day_month, last_day_month
                        )
                    )
                ), Value(Decimal('0'))),
            total_commissions=Count(
                'commissions',
                filter=Q(commissions__sale__date__range=(first_day_month, last_day_month))
            ),
        ).prefetch_related(
            Prefetch(
                'commissions',
                queryset=Commission.objects.select_related(
                    'sale__product', 'sale__store__city__region', 'percentage'
                ).prefetch_related(
                    'percentage__formula'
                ).filter(sale__date__range=(first_day_month, last_day_month)),
                to_attr='commissions_set'
            )
        ).first()
        if not user_commissions:
            return status.HTTP_204_NO_CONTENT
        commissions = UserCommissionSerializer(user_commissions).data
        commissions['start'] = first_day_month.strftime('%Y-%m-%d')
        commissions['end'] = last_day_month.strftime('%Y-%m-%d')
        return Response(commissions)
