from django.urls import path
from . import views

urlpatterns = [
    path('', views.finances_dashboard, name='finances_dashboard'),
]
