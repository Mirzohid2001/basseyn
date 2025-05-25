# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about_view, name="about"),
    path('contacts/', views.contacts, name="contacts"),
    path('faq/', views.faq, name="faq"),
    path('<slug:slug>/', views.info_page, name="info_page"),
]

