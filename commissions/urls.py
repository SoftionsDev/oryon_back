from django.urls import path
from .views import get_commissions

urlpatterns = [
    path('', get_commissions, name='get_commissions'),
]
