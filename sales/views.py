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
            permission_classes = [IsAdmin|IsManager]
        return [permission() for permission in permission_classes]

    def get(self, request):
        sales = Sale.objects.select_related(
            'user', 'product', 'store'
        ).all()
        serializer = SaleReadSerializer(sales, many=True)
        return Response(serializer.data)

    def post(self, request):
        if isinstance(request.data, list):
            serializer = SalesWriteSerializer(data=request.data, many=True)
        else:
            serializer = SalesWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SalesCreateBatch(UploadCSV):
    """
    Reuse the POST method to receive a CSV file and create sales
    must implement the process_data method
    """

    permission_classes = [IsAdmin|IsManager]
    serializer_class = SalesWriteSerializer
    field_mapping = {
        'ID_UNICO': 'commercial',
        'VITRINA': 'store',
        'PRODUCTO': 'product',
        'FECHA_VENTA': 'date',
        'VALOR': 'price'
    }


