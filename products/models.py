from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="category_images/", blank=True, null=True, verbose_name="Изображение категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Product(models.Model):
    class Availability(models.TextChoices):
        IN_STOCK = "in_stock", "В наличии"
        ON_ORDER = "on_order", "Под заказ"

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=160, unique=True, blank=True, help_text="По умолчанию = id; можно менять.")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    availability = models.CharField(
        max_length=20,
        choices=Availability.choices,
        default=Availability.IN_STOCK,
        verbose_name="Наличие"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)
        if creating and not self.slug:
            self.slug = str(self.pk)
            super().save(update_fields=['slug'])

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/")
    alt_text = models.CharField(max_length=120, blank=True)

class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)
    name = models.CharField('Параметр', max_length=255)
    value = models.CharField('Значение', max_length=255)

    def __str__(self):
        return f"{self.name}: {self.value}"

