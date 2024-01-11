from django.urls import path

from utils import views

urlpatterns = [
    path('fields/', views.Fields.as_view(), name='fields')
]
