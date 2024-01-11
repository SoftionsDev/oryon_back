from django.urls import re_path
from rest_framework.routers import DefaultRouter
from users.views import CommercialViewSet

router = DefaultRouter()
router.register(r'', CommercialViewSet)

urlpatterns = [
    re_path(
        r'(?P<user__email>[\w\.-]+@[\w\.-]+\.\w+)',
        CommercialViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
        name='commercial-detail'
    )
] + router.urls
