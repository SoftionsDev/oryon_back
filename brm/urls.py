from django.urls import path
from .views import RuleViews

urlpatterns = [
    path('', RuleViews.as_view(), name='rules'),
    path('<uuid:id>/', RuleViews.as_view(), name='rules-delete')
]
