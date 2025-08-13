from django.contrib import admin


from .models import Category, Product, ProductImage, ProductCharacteristic, SEOSettings

from django.db import models
from django.forms import Textarea

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "image_preview")
    search_fields = ("name",)
    fields = ("name", "description", "image")

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px;">'
        return "Нет изображения"
    image_preview.short_description = "Превью"
    image_preview.allow_tags = True

class ProductCharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "availability", "is_featured", "created_at")
    search_fields = ("name", "category__name")
    list_filter = ("category", "is_featured", "availability")
    inlines = [ProductImageInline, ProductCharacteristicInline]



@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("page_name", "title", "canonical")
    search_fields = ("page_name", "title")

    # Показываем все поля
    fields = ("page_name", "title", "description", "canonical")

    # Делаем Textarea для description
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "style": "width:100%;"})},
    }
