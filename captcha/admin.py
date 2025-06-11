from django.contrib import admin
from .models import CaptchaImage, CaptchaQuestion, CaptchaSession

@admin.register(CaptchaImage)
class CaptchaImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'image', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('category',)

@admin.register(CaptchaQuestion)
class CaptchaQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_type', 'question_text', 'correct_answer', 'is_active')
    list_filter = ('question_type', 'is_active')
    search_fields = ('question_text', 'correct_answer')

@admin.register(CaptchaSession)
class CaptchaSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'created_at', 'expires_at', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('session_key',)
    readonly_fields = ('created_at', 'expires_at')
