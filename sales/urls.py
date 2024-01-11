from django.urls import path
from sales import views

urlpatterns = [
    path('', views.SalesViews.as_view(), name='sales'),
    path('<uuid:id>/', views.SalesViews.as_view(), name='sales-id'),
    path('upload/', views.SalesCreateBatch.as_view(), name='upload-sales'),
]

