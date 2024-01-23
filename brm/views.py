from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from brm.models import Percentages, Formula
from brm.serializers import (
    PercentagesReadSerializer, PercentagesWriteSerializer,
    FormulaReadSerializer, FormulaWriteSerializer
)
from utils.permissions import IsAdmin, IsManager


class PercentagesViews(APIView):
    permission_classes = [IsAdmin | IsManager]

    def get(self, request, *args, **kwargs):
        serializer = PercentagesReadSerializer(Percentages.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PercentagesWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        percentage = Percentages.objects.filter(id=id).first()
        if percentage:
            percentage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormulaView(APIView):
    permission_classes = [IsAdmin | IsManager]

    def get(self, request, *args, **kwargs):
        serializer = FormulaReadSerializer(
            Formula.objects.select_related('rule'), many=True
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = FormulaWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        formula = Formula.objects.filter(id=id).first()
        if formula:
            formula.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)