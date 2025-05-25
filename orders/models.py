from django.db import models
from products.models import Product
from services.models import Service

class Order(models.Model):
    client_name = models.CharField(max_length=120)
    client_phone = models.CharField(max_length=40)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'Новый'),
            ('in_progress', 'В обработке'),
            ('done', 'Выполнен'),
        ],
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ {self.client_name} ({self.created_at.date()})"

class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=40)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
