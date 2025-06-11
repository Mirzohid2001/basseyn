from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import CaptchaQuestion, CaptchaSession, CaptchaImage
import json
import random

def get_captcha(request):
    """Yangi captcha olish"""
    # Tasodifiy savol turini tanlash
    question_type = random.choice(['text', 'image'])
    
    if question_type == 'text':
        # Matematik savol yaratish
        math_question = CaptchaQuestion.generate_math_question()
        question_text = math_question['question']
        answer = math_question['answer']
        
        # Sessiya yaratish
        session = CaptchaSession.create_session(None, answer)
        
        return JsonResponse({
            'success': True,
            'session_key': session.session_key,
            'type': 'text',
            'question': question_text,
            'expires_at': session.expires_at.timestamp()
        })
    else:
        # Rasmli savol olish
        questions = CaptchaQuestion.objects.filter(question_type='image', is_active=True)
        
        if not questions.exists():
            # Rasmli savol topilmasa, matematik savol qaytarish
            math_question = CaptchaQuestion.generate_math_question()
            question_text = math_question['question']
            answer = math_question['answer']
            
            # Sessiya yaratish
            session = CaptchaSession.create_session(None, answer)
            
            return JsonResponse({
                'success': True,
                'session_key': session.session_key,
                'type': 'text',
                'question': question_text,
                'expires_at': session.expires_at.timestamp()
            })
        
        # Tasodifiy rasmli savolni tanlash
        question = random.choice(questions)
        
        # Tegishli kategoriyaga oid rasmlarni olish
        images = CaptchaImage.objects.filter(
            category=question.image_category, 
            is_active=True
        )
        
        if not images.exists():
            # Rasmlar topilmasa, matematik savol qaytarish
            math_question = CaptchaQuestion.generate_math_question()
            question_text = math_question['question']
            answer = math_question['answer']
            
            # Sessiya yaratish
            session = CaptchaSession.create_session(None, answer)
            
            return JsonResponse({
                'success': True,
                'session_key': session.session_key,
                'type': 'text',
                'question': question_text,
                'expires_at': session.expires_at.timestamp()
            })
        
        # Tasodifiy 6 ta rasmni tanlash
        selected_images = random.sample(list(images), min(6, len(images)))
        
        # Sessiya yaratish
        session = CaptchaSession.create_session(question, question.correct_answer)
        
        return JsonResponse({
            'success': True,
            'session_key': session.session_key,
            'type': 'image',
            'question': question.question_text,
            'images': [{'id': img.id, 'url': img.image.url} for img in selected_images],
            'expires_at': session.expires_at.timestamp()
        })

def verify_captcha(request):
    """Captcha javobini tekshirish"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    try:
        # POST so'rovini tekshirish
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            session_key = data.get('session_key')
            answer = data.get('answer')
        else:
            # Form data
            session_key = request.POST.get('session_key')
            answer = request.POST.get('answer')
        
        if not session_key or not answer:
            return JsonResponse({'success': False, 'error': 'Missing required parameters'})
        
        # Sessiyani topish
        try:
            session = CaptchaSession.objects.get(session_key=session_key)
        except CaptchaSession.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid session key'})
        
        # Sessiya muddati tugaganini tekshirish
        if session.is_expired():
            return JsonResponse({'success': False, 'error': 'Session expired'})
        
        # Javobni tekshirish
        if session.is_verified:
            return JsonResponse({'success': True, 'message': 'Session already verified'})
        
        # Javob to'g'riligini tekshirish
        if str(answer).strip().lower() == str(session.correct_answer).strip().lower():
            session.is_verified = True
            session.save()
            return JsonResponse({'success': True, 'message': 'Captcha verified successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'Incorrect answer'})
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
