from django.db import models
from products.models import Product
from services.models import Service

class Order(models.Model):
    client_name = models.CharField(max_length=120)
    client_phone = models.CharField(max_length=40)
    client_email = models.EmailField(blank=True)
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


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.DecimalField(max_digits=12, decimal_places=2)

    def line_total(self):
        return (self.price_at_time or 0) * self.quantity

class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=40)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
