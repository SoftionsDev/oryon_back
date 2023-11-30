from django.urls import path
from rest_framework.routers import DefaultRouter

from commissions.views import CommissionViews

router = DefaultRouter()
router.register('', CommissionViews, basename='commissions')

urlpatterns = [] + router.urls
