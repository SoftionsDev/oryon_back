from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, UserToken

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('token/', UserToken.as_view(), name='token_obtain_pair'),
] + router.urls