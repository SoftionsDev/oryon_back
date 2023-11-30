from django.urls import path
from .views import RuleViews

urlpatterns = [
    path('', RuleViews.as_view(), name='rules'),
]
