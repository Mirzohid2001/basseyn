# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<slug:slug>/", views.product_detail_by_slug, name="product_detail"),  # ← сначала slug
    path("<int:pk>/", views.product_detail_legacy, name="product_detail_legacy"),  # потом legacy по id
]
