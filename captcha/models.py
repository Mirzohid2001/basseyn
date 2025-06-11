from django.db import models
from django.utils import timezone
import datetime
import random
import string

class CaptchaImage(models.Model):
    """Rasmli captcha uchun tasvirlar"""
    category = models.CharField(max_length=100, verbose_name="Kategoriya")
    image = models.ImageField(upload_to='captcha_images/', verbose_name="Rasm")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    class Meta:
        verbose_name = "Captcha rasm"
        verbose_name_plural = "Captcha rasmlar"
    
    def __str__(self):
        return f"{self.category} - {self.id}"

class CaptchaQuestion(models.Model):
    """Matnli va rasmli savollar"""
    QUESTION_TYPES = (
        ('text', 'Matnli savol'),
        ('image', 'Rasmli savol'),
    )
    
    question_type = models.CharField(max_length=5, choices=QUESTION_TYPES, verbose_name="Savol turi")
    question_text = models.CharField(max_length=255, verbose_name="Savol matni")
    correct_answer = models.CharField(max_length=100, verbose_name="To'g'ri javob")
    image_category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Rasm kategoriyasi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    class Meta:
        verbose_name = "Captcha savol"
        verbose_name_plural = "Captcha savollar"
    
    def __str__(self):
        return self.question_text
    
    @classmethod
    def generate_math_question(cls):
        """Matematik savol yaratish"""
        operations = ['+', '-', '*']
        operation = random.choice(operations)
        
        if operation == '+':
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            answer = a + b
            question = f"Сколько будет {a} + {b}?"
        elif operation == '-':
            a = random.randint(5, 20)
            b = random.randint(1, a)
            answer = a - b
            question = f"Сколько будет {a} - {b}?"
        else:  # multiplication
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            answer = a * b
            question = f"Сколько будет {a} × {b}?"
            
        return {
            'question': question,
            'answer': str(answer)
        }

class CaptchaSession(models.Model):
    """Foydalanuvchi sessiyalarini boshqarish"""
    session_key = models.CharField(max_length=40, unique=True, verbose_name="Sessiya kaliti")
    question = models.ForeignKey(CaptchaQuestion, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Savol")
    correct_answer = models.CharField(max_length=100, verbose_name="To'g'ri javob")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    expires_at = models.DateTimeField(verbose_name="Tugash vaqti")
    is_verified = models.BooleanField(default=False, verbose_name="Tekshirilgan")
    
    class Meta:
        verbose_name = "Captcha sessiya"
        verbose_name_plural = "Captcha sessiyalar"
    
    def __str__(self):
        return self.session_key
    
    @classmethod
    def generate_session_key(cls):
        """Tasodifiy sessiya kaliti yaratish"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=40))
    
    @classmethod
    def create_session(cls, question, answer, expiry_minutes=30):
        """Yangi captcha sessiyasini yaratish"""
        session_key = cls.generate_session_key()
        expires_at = timezone.now() + datetime.timedelta(minutes=expiry_minutes)
        
        session = cls(
            session_key=session_key,
            question=question if isinstance(question, CaptchaQuestion) else None,
            correct_answer=answer,
            expires_at=expires_at
        )
        session.save()
        
        return session
    
    def is_expired(self):
        """Sessiya muddati tugaganini tekshirish"""
        return timezone.now() > self.expires_at
