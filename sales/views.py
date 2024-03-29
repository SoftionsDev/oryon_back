from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sales.models import Sale
from sales.serializers import SalesWriteSerializer, SaleReadSerializer
from utils.permissions import IsManager, IsAdmin
from utils.views import UploadCSV


class SalesViews(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin | IsManager]
        return [permission() for permission in permission_classes]

    def get(self, request, id=None):
        sales = Sale.objects.select_related(
            'user', 'product', 'store'
        ).all()
        if id:
            sales = sales.filter(id=id).first()
            serializer = SalesWriteSerializer(sales)
            return Response(serializer.data)
        serializer = SaleReadSerializer(sales, many=True)
        return Response(serializer.data)

    def post(self, request, id=None):
        if isinstance(request.data, list):
            serializer = SalesWriteSerializer(data=request.data, many=True)
        else:
            serializer = SalesWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id=None):
        if not id:
            return Response(status=status.HTTP_204_NO_CONTENT)
        sale = get_object_or_404(Sale, id=id)
        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SalesCreateBatch(UploadCSV):
    """
    Reuse the POST method to receive a CSV file and create sales
    must implement the process_data method
    """

    permission_classes = [IsAdmin | IsManager]
    serializer_class = SalesWriteSerializer
    field_mapping = {
        'ID_UNICO': 'user_id',
        'VITRINA': 'store_id',
        'PRODUCTO': 'product_id',
        'FECHA_VENTA': 'date',
        'VALOR': 'price',
        'COMISION': 'commission_type',
        'TIPO VENTA': 'type'
    }


