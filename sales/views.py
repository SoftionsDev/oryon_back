from rest_framework import viewsets

from sales.models import Sale
from sales.serializers import SaleSerializer
from utils.permissions import IsManager, IsCollaborator


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsManager, IsCollaborator]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
