from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, UserToken, CommercialViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'commercial', CommercialViewSet)

urlpatterns = [
    path('token/', UserToken.as_view(), name='token_obtain_pair'),
] + router.urls