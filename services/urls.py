# services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name="service_list"),
    path('services/<int:pk>/', views.service_detail, name="service_detail"),
    path('projects/', views.project_list, name="project_list"),
    path('projects/<int:pk>/', views.project_detail, name="project_detail"),
]
