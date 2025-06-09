from django.urls import path
from . import views

urlpatterns = [
    path('get-captcha/', views.get_captcha, name='get_captcha'),
    path('verify-captcha/', views.verify_captcha, name='verify_captcha'),
]
