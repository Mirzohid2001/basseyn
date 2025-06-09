from django.contrib import admin
from .models import CaptchaQuestion, CaptchaSession, CaptchaImage

# @admin.register(CaptchaImage)
# class CaptchaImageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'category', 'is_active', 'image_preview')
#     list_filter = ('category', 'is_active')
#     search_fields = ('category',)
    
#     def image_preview(self, obj):
#         if obj.image:
#             return f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover;" />'
#         return "-"
    
#     image_preview.allow_tags = True
#     image_preview.short_description = 'Предпросмотр'

@admin.register(CaptchaQuestion)
class CaptchaQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_type', 'target_category', 'difficulty', 'is_active')
    list_filter = ('question_type', 'difficulty', 'is_active', 'target_category')
    search_fields = ('question', 'answer', 'target_category')

@admin.register(CaptchaSession)
class CaptchaSessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'question', 'created_at', 'is_solved')
    list_filter = ('is_solved', 'created_at')
    readonly_fields = ('session_key', 'question', 'created_at', 'image_captcha_data')
    search_fields = ('session_key',)
    
    def has_add_permission(self, request):
        return False
