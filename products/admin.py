from django.contrib import admin
from .models import Category, Product, ProductImage

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

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_featured", "created_at")
    search_fields = ("name", "category__name")
    list_filter = ("category", "is_featured")
    inlines = [ProductImageInline]
