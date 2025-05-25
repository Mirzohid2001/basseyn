from django.contrib import admin
from .models import Order, ContactRequest

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("client_name", "client_phone", "product", "service", "status", "created_at")
    list_filter = ("status", "created_at", "product", "service")
    search_fields = ("client_name", "client_phone")

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "created_at")
    search_fields = ("name", "phone")
