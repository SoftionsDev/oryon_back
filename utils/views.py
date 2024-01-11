import csv
import io

from django.apps import apps
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from utils.permissions import IsAdmin, IsManager


class UploadCSV(APIView):

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = None
    field_mapping: dict

    def post(self, request):
        if 'file' not in request.data:
            return Response(
                {
                    'error':
                        'No file provided, '
                        'ensure that you have uploaded with parameter name file'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.data['file']
        data_set = file.read().decode('utf-8-sig')
        io_string = io.StringIO(data_set)

        assert self.field_mapping, 'field_mapping is not defined'

        with io_string as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            data = [
                {
                    self.field_mapping[k]: v
                    for k, v in row.items()
                    if k in self.field_mapping
                }
                for row in reader
            ]
            if self.serializer_class:
                serializer = self.serializer_class(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class Fields(APIView):
    permission_classes = [IsAdmin | IsManager]

    def get(self, request, format=None):
        models = apps.get_models()
        model_fields = {}

        excluded_fields = {
            'User': [
                'password', 'last_login', 'is_superuser', 'is_staff', 'photo'
            ],
            'Sale': ['created_at', 'updated_at'],
        }

        for model in models:
            if 'django.' in str(model) and model != User:
                continue

            model_name = model.__name__
            fields = [
                field.name for field in model._meta.fields
                if field.name not in excluded_fields.get(model_name, [])
                and field.get_internal_type() != 'ForeignKey'
            ]
            model_fields[model_name] = fields

        return Response(model_fields)
