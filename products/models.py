from django.db import models

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

class SEOSettings(models.Model):
    page_name = models.CharField(
        "URL name страницы",
        max_length=100,
        unique=True,
        help_text="Имя маршрута (url_name) из urls.py. Например: home, product_list, product_detail"
    )
    title = models.CharField(
        "Title",
        max_length=255,
        blank=True,
        help_text="Заголовок страницы (<title>)"
    )
    description = models.TextField(
        "Meta description",
        blank=True,
        help_text="Описание страницы (meta description)"
    )
    canonical = models.URLField(
        "Canonical URL",
        blank=True,
        help_text="Каноническая ссылка на страницу"
    )

    class Meta:
        verbose_name = "SEO-настройка"
        verbose_name_plural = "SEO-настройки"

    def __str__(self):
        return f"{self.page_name} — {self.title or 'Без title'}"