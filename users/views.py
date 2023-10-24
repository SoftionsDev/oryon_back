from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):

    model = User
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('groups').all()
