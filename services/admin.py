from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import Service, ServiceImage, Project, ProjectImage

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_featured")
    search_fields = ("name",)
    list_filter = ("is_featured",)
    inlines = [ServiceImageInline]

    # чтобы точно было видно поле seo_description
    fieldsets = (
        (None, {"fields": ("name", "price", "is_featured")}),
        ("Контент", {"fields": ("description", "characteristics")}),
        ("SEO", {"fields": ("seo_description",)}),
    )

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "style": "width:100%;"})},
    }

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "date_completed", "is_featured")
    inlines = [ProjectImageInline]

