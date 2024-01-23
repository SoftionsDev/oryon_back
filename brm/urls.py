from django.urls import path
from .views import PercentagesViews, FormulaView

urlpatterns = [
    path('percentages/', PercentagesViews.as_view(), name='rules'),
    path('percentages/<uuid:id>/', PercentagesViews.as_view(), name='rules-delete'),
    path('formula/', FormulaView.as_view(), name='formula'),
    path('formula/<uuid:id>/', FormulaView.as_view(), name='formula-delete'),
]
