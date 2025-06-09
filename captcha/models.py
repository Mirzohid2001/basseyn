from django.db import models
import random
import string
import uuid
import os
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

def captcha_image_path(instance, filename):
    # Генерируем уникальное имя файла для изображения CAPTCHA
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('captcha_images', filename)

class CaptchaImage(models.Model):
    image = models.ImageField(upload_to=captcha_image_path)
    category = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.category} ({self.id})"

class CaptchaQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('text', 'Текстовый вопрос'),
        ('image', 'Выбор изображений'),
    ]
    
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=50, blank=True)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='text')
    target_category = models.CharField(max_length=50, blank=True, help_text='Категория изображений для выбора (для image типа)')
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ], default='medium')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.question
    
    @classmethod
    def get_random_question(cls):
        # Try to get a random active text question
        active_questions = cls.objects.filter(is_active=True, question_type='text')
        if active_questions.exists():
            return random.choice(active_questions)
        
        # If no active questions, create a simple math question
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operation = random.choice(['+', '-', '*'])
        
        if operation == '+':
            answer = a + b
            question = f"Сколько будет {a} + {b}?"
        elif operation == '-':
            # Ensure positive result
            if a < b:
                a, b = b, a
            answer = a - b
            question = f"Сколько будет {a} - {b}?"
        else:  # multiplication
            answer = a * b
            question = f"Сколько будет {a} × {b}?"
        
        # Create a temporary question object (not saved to database)
        return cls(question=question, answer=str(answer), difficulty='medium', question_type='text')
        
    def get_image_captcha_data(self):
        """Возвращает данные для CAPTCHA с изображениями"""
        if self.question_type != 'image':
            return None
        
        # Получаем изображения целевой категории (которые нужно выбрать)
        target_images = list(CaptchaImage.objects.filter(
            category=self.target_category,
            is_active=True
        )[:4])  # Максимум 4 целевых изображения
        
        # Если нет изображений целевой категории, вернуть None
        if len(target_images) < 1:
            return None
        
        # Получаем другие изображения для отвлечения
        other_images = list(CaptchaImage.objects.filter(
            is_active=True
        ).exclude(category=self.target_category)[:9-len(target_images)])  # Всего будет 9 изображений
        
        # Если недостаточно изображений, дублируем имеющиеся
        if len(target_images) + len(other_images) < 4:
            # Дублируем целевые изображения, если их мало
            while len(target_images) < 2 and len(target_images) > 0:
                target_images.append(target_images[0])
            
            # Если нет других изображений, используем дубликаты целевых
            if not other_images and target_images:
                # Создаем копии целевых изображений для других категорий
                for i in range(2):
                    other_images.append(target_images[0])
    
        # Объединяем и перемешиваем изображения
        all_images = target_images + other_images
        random.shuffle(all_images)
        
        # Создаем данные для фронтенда
        image_data = []
        correct_indices = []
        
        for i, img in enumerate(all_images):
            image_data.append({
                'id': img.id,
                'url': img.image.url,
                'category': img.category
            })
            
            if img.category == self.target_category:
                correct_indices.append(i)
        
        return {
            'images': image_data,
            'correct_indices': correct_indices
        }

class CaptchaSession(models.Model):
    session_key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    question = models.ForeignKey(CaptchaQuestion, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_solved = models.BooleanField(default=False)
    image_captcha_data = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"Session {self.session_key[:8]}... - {'Solved' if self.is_solved else 'Unsolved'}"
    
    @classmethod
    def create_new_session(cls):
        # Get a random question
        question = CaptchaQuestion.get_random_question()
        
        # Create a new session
        session = cls.objects.create(question=question)
        
        # If it's an image captcha, generate the image data
        if question.question_type == 'image':
            image_data = question.get_image_captcha_data()
            if image_data:
                session.image_captcha_data = image_data
                session.save()
        
        # Clean up old sessions
        cls.cleanup_old_sessions()
        
        return session
    
    @classmethod
    def cleanup_old_sessions(cls):
        # Remove sessions older than 1 hour
        expiration_time = timezone.now() - timedelta(hours=1)
        cls.objects.filter(created_at__lt=expiration_time).delete()
    
    def verify_answer(self, user_answer):
        # If already solved, return True
        if self.is_solved:
            return True
        
        # For text-based captcha
        if self.question.question_type == 'text':
            # Compare answers (case-insensitive)
            if user_answer.lower().strip() == self.question.answer.lower().strip():
                self.is_solved = True
                self.save()
                return True
        
        # For image-based captcha
        elif self.question.question_type == 'image' and self.image_captcha_data:
            try:
                # user_answer should be a comma-separated list of indices
                selected_indices = [int(idx) for idx in user_answer.split(',')]
                correct_indices = self.image_captcha_data.get('correct_indices', [])
                
                # Check if the selected indices match the correct ones
                if sorted(selected_indices) == sorted(correct_indices):
                    self.is_solved = True
                    self.save()
                    return True
            except (ValueError, AttributeError):
                # If there's an error parsing the answer, it's wrong
                pass
        
        return False
