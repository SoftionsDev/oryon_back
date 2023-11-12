from django.urls import path
from sales import views

urlpatterns = [
    path('', views.SalesViews.as_view(), name='sales'),
    path('upload/', views.SalesCreateBatch.as_view(), name='upload-sales'),
]

