from rest_framework import viewsets
import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from utils.permissions import IsAdmin, IsManager
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin|IsManager]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

class ProductUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdmin|IsManager]

    def post(self, request):
        if 'file' not in request.data:
            return Response(
            {
                    'error': 'No file provided, ensure that you have uploaded with parameter name file'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.data['file']
        data_set = file.read().decode('utf-8-sig')
        io_string = io.StringIO(data_set)

        # TODO seek for a better way to do this
        field_mapping = {
            'Código de producto': 'code',
            'Descripción de producto': 'name',
            'Código de Categoría': 'category',
            'Descripción de categoría': 'category_description',
            'Código de Marca': 'brand',
            'Descripción de marca': 'brand_description',
            'Valor de venta': 'price'
        }

        with io_string as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                product_data = {field_mapping[k]: v for k, v in row.items() if k in field_mapping}
                Product.objects.update_or_create(**product_data)

        return Response(status=status.HTTP_201_CREATED)
