from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from brm.models import Rule
from brm.serializers import RuleWriteSerializer, RuleReadSerializer
from utils.permissions import IsAdmin, IsManager


class RuleViews(APIView):
    permission_classes = [IsAdmin | IsManager]

    def get(self, request, *args, **kwargs):
        serializer = RuleReadSerializer(Rule.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RuleWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {'message': 'Rule is valid and formula created'}
        return Response(message, status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        rule = Rule.objects.filter(id=id).first()
        if not rule:
            return Response(status=status.HTTP_204_NO_CONTENT)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)