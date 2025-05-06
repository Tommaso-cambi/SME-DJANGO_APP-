from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders_dashboard, name='orders_dashboard'),
]
