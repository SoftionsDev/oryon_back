from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserSerializer, TokenSerializer
from utils.permissions import IsAdmin, IsManager


class UserViewSet(ModelViewSet):

    model = User
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('groups').all()
    permission_classes = [IsAdmin|IsManager]


class UserToken(TokenObtainPairView):
    serializer_class = TokenSerializer