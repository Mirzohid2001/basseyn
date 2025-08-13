from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.html import format_html

from .models import ContactInfo, InfoPage, About, Banner, BannerImage, SEOSettings, Projectt


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("address", "phone", "email","telegram")

@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')

class BannerImageInline(admin.TabularInline):
    model = BannerImage
    extra = 1

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [BannerImageInline]

@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    # Явно показываем все поля — и на странице "Add", и на "Change"
    fields = ("page_name", "title", "description", "canonical")

    list_display = ("page_name", "title", "canonical")
    search_fields = ("page_name", "title")
    save_on_top = True


@admin.register(Projectt)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    fields = ("title", "description", "image", "order", "is_active")
    readonly_fields = ()

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;width:70px;object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return "—"
    thumb.short_description = "Превью"


