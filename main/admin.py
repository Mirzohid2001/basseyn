from django.contrib import admin
from .models import ContactInfo, InfoPage, About, Banner, BannerImage


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
