from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import CaptchaSession
import uuid
import json

@require_http_methods(["GET"])
def get_captcha(request):
    """
    Generate a new CAPTCHA question and return it as JSON
    """
    # Create a new session
    session = CaptchaSession.create_new_session()
    
    response_data = {
        'success': True,
        'session_key': str(session.session_key),
        'question': session.question.question,
        'question_type': session.question.question_type,
    }
    
    # If it's an image captcha, include the image data
    if session.question.question_type == 'image' and session.image_captcha_data:
        response_data['image_data'] = session.image_captcha_data['images']
        response_data['target_category'] = session.question.target_category
    
    # Return the question and session key
    return JsonResponse(response_data)

@require_http_methods(["POST"])
def verify_captcha(request):
    """
    Verify a CAPTCHA answer
    """
    # Try to get data from POST or JSON body
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                session_key = data.get('session_key')
                answer = data.get('answer')
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'message': 'Неверный формат JSON'
                }, status=400)
        else:
            session_key = request.POST.get('session_key')
            answer = request.POST.get('answer')
    else:
        return JsonResponse({
            'success': False,
            'message': 'Метод не поддерживается'
        }, status=405)
    
    if not session_key or not answer:
        return JsonResponse({
            'success': False,
            'message': 'Недостаточно данных для проверки CAPTCHA'
        }, status=400)
    
    try:
        session = CaptchaSession.objects.get(session_key=session_key)
        
        if session.verify_answer(answer):
            return JsonResponse({
                'success': True,
                'message': 'Правильный ответ!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Неправильный ответ. Попробуйте еще раз.'
            })
    except CaptchaSession.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Недействительная сессия CAPTCHA'
        }, status=400)
