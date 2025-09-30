# orders/urls.py
from django.shortcuts import redirect
from django.urls import path
from . import views


def redirect_old_order(request):
    return redirect("/order/?product=" + request.GET.get("product", ""), permanent=True)

urlpatterns = [
    path('', views.order_create, name="order_create"),
    path("order/", redirect_old_order),
    path('contact/', views.contact_request, name="contact_request"),
    path('cart/', views.cart_detail, name="cart_detail"),
    path('cart/add/<int:product_id>/', views.cart_add, name="cart_add"),
    path('cart/remove/<int:product_id>/', views.cart_remove, name="cart_remove"),
    path('cart/update/<int:product_id>/', views.cart_update, name="cart_update"),
    path('checkout/', views.checkout, name="checkout"),
    path('checkout/success/', views.checkout_success, name="checkout_success"),
    path('my-orders/', views.my_orders, name="my_orders"),
    path('my-orders/set-lookup/', views.my_orders_set_lookup, name="my_orders_set_lookup"),
    path('my-orders/<int:pk>/', views.order_detail, name="order_detail"),
]
