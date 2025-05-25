# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.order_create, name="order_create"),
    path('contact/', views.contact_request, name="contact_request"),
]
