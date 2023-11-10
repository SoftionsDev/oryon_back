from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserSerializer, TokenSerializer, CommercialSerializer
from utils.permissions import IsAdmin, IsManager
from users.models import User, Commercial


class UserViewSet(ModelViewSet):

    model = User
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('groups').all()
    permission_classes = [IsAdmin|IsManager]


class UserToken(TokenObtainPairView):
    serializer_class = TokenSerializer


class CommercialViewSet(ModelViewSet):

    model = Commercial
    serializer_class = CommercialSerializer
    queryset = Commercial.objects.select_related('user', 'manager').all()
    permission_classes = [IsAdmin|IsManager]
    lookup_field = 'user__email'

    def get_queryset(self):
        if self.request.user.is_admin:
            return Commercial.objects.select_related(
                'user', 'manager'
            ).all()

        # it has to be a manager to retrieve other commercials
        manager_id = self.request.user.code
        return Commercial.objects.filter(
            manager_id=manager_id
        ).select_related('user', 'manager')