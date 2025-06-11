from django.db import models
from django.utils import timezone
import datetime
import random
import string

class CaptchaImage(models.Model):
    """Rasmli captcha uchun tasvirlar"""
    category = models.CharField(max_length=100, verbose_name="Категория")
    image = models.ImageField(upload_to='captcha_images/', verbose_name="Фото")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Captcha фото"
        verbose_name_plural = "Captcha фотографии"
    
    def __str__(self):
        return f"{self.category} - {self.id}"

class CaptchaQuestion(models.Model):
    """Matnli va rasmli savollar"""
    QUESTION_TYPES = (
        ('text', 'Текстовый вопрос'),
        ('image', 'Вопрос с фотографией'),
    )
    
    question_type = models.CharField(max_length=5, choices=QUESTION_TYPES, verbose_name="Тип вопроса")
    question_text = models.CharField(max_length=255, verbose_name="Текст вопроса")
    correct_answer = models.CharField(max_length=100, verbose_name="Правильный ответ")
    image_category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Категория фото")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    
    class Meta:
        verbose_name = "Captcha вопрос"
        verbose_name_plural = "Captcha вопросы"
    
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
    session_key = models.CharField(max_length=40, unique=True, verbose_name="Ключ сессии")
    question = models.ForeignKey(CaptchaQuestion, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Вопрос")
    correct_answer = models.CharField(max_length=100, verbose_name="Правильный ответ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    expires_at = models.DateTimeField(verbose_name="Время окончания")
    is_verified = models.BooleanField(default=False, verbose_name="Проверен")
    
    class Meta:
        verbose_name = "Captcha сессия"
        verbose_name_plural = "Captcha сессии"
    
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
