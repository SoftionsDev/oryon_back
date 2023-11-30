from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from brm.serializers import RuleSerializer
from utils.permissions import IsAdmin, IsManager


class RuleViews(APIView):
    permission_classes = [IsAdmin | IsManager]

    def post(self, request, *args, **kwargs):
        serializer = RuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {'message': 'Rule is valid'}
        return Response(message, status=status.HTTP_201_CREATED)