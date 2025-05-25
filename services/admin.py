from django.contrib import admin
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
    inlines = [ServiceImageInline]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "date_completed", "is_featured")
    inlines = [ProjectImageInline]
