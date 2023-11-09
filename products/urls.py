from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductUploadView

router = DefaultRouter()
router.register(r'', ProductViewSet)

urlpatterns = [
    path('upload-products/', ProductUploadView.as_view(), name='upload-products'),
] + router.urls

