# orders/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Order, ContactRequest
from products.models import Product
from services.models import Service
from captcha.models import CaptchaSession
import json

def order_create(request):
    products = Product.objects.all()
    services = Service.objects.all()
    
    if request.method == "POST":
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                name = request.POST.get("client_name")
                phone = request.POST.get("client_phone")
                comment = request.POST.get("comment", "")
                product_id = request.POST.get("product")
                service_id = request.POST.get("service")
                session_key = request.POST.get("captcha_session_key")
                captcha_answer = request.POST.get("captcha_answer")
                
                # Validate required fields
                if not name or not phone:
                    return JsonResponse({
                        'success': False,
                        'error': 'Имя и телефон обязательны для заполнения'
                    }, status=400)
                
                # Validate CAPTCHA
                if not session_key or not captcha_answer:
                    return JsonResponse({
                        'success': False,
                        'error': 'Пожалуйста, заполните CAPTCHA'
                    }, status=400)
                
                try:
                    captcha_session = CaptchaSession.objects.get(session_key=session_key)
                    if not captcha_session.is_solved and not captcha_session.verify_answer(captcha_answer):
                        return JsonResponse({
                            'success': False,
                            'error': 'Неверный ответ CAPTCHA'
                        }, status=400)
                except CaptchaSession.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Недействительная сессия CAPTCHA'
                    }, status=400)
                
                order = Order(
                    client_name=name,
                    client_phone=phone,
                    comment=comment
                )
                
                if product_id:
                    order.product_id = product_id
                if service_id:
                    order.service_id = service_id
                    
                order.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Заказ успешно отправлен! Мы свяжемся с вами в ближайшее время.'
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': 'Произошла ошибка при обработке заказа'
                }, status=500)
        else:
            # Regular form submission
            name = request.POST.get("client_name")
            phone = request.POST.get("client_phone")
            comment = request.POST.get("comment", "")
            product_id = request.POST.get("product")
            service_id = request.POST.get("service")
            session_key = request.POST.get("captcha_session_key")
            captcha_answer = request.POST.get("captcha_answer")
            
            # Validate CAPTCHA
            try:
                captcha_session = CaptchaSession.objects.get(session_key=session_key)
                if not captcha_session.is_solved and not captcha_session.verify_answer(captcha_answer):
                    # If CAPTCHA is invalid, redirect back to the form with an error
                    return render(request, "orders/order_form.html", {
                        "products": products, 
                        "services": services,
                        "error": "Неверный ответ CAPTCHA. Пожалуйста, попробуйте еще раз."
                    })
            except CaptchaSession.DoesNotExist:
                # If CAPTCHA session doesn't exist, redirect back to the form with an error
                return render(request, "orders/order_form.html", {
                    "products": products, 
                    "services": services,
                    "error": "Недействительная сессия CAPTCHA. Пожалуйста, попробуйте еще раз."
                })
            
            order = Order(
                client_name=name,
                client_phone=phone,
                comment=comment
            )
            if product_id:
                order.product_id = product_id
            if service_id:
                order.service_id = service_id
            order.save()
            return render(request, "orders/order_success.html")
            
    return render(request, "orders/order_form.html", {
        "products": products, 
        "services": services
    })

def contact_request(request):
    if request.method == "POST":
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                name = request.POST.get("name")
                phone = request.POST.get("phone")
                message = request.POST.get("message", "")
                session_key = request.POST.get("captcha_session_key")
                captcha_answer = request.POST.get("captcha_answer")
                
                # Validate required fields
                if not name or not phone:
                    return JsonResponse({
                        'success': False,
                        'error': 'Имя и телефон обязательны для заполнения'
                    }, status=400)
                
                # Validate CAPTCHA
                if not session_key or not captcha_answer:
                    return JsonResponse({
                        'success': False,
                        'error': 'Пожалуйста, заполните CAPTCHA'
                    }, status=400)
                
                try:
                    captcha_session = CaptchaSession.objects.get(session_key=session_key)
                    if not captcha_session.is_solved and not captcha_session.verify_answer(captcha_answer):
                        return JsonResponse({
                            'success': False,
                            'error': 'Неверный ответ CAPTCHA'
                        }, status=400)
                except CaptchaSession.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Недействительная сессия CAPTCHA'
                    }, status=400)
                
                ContactRequest.objects.create(
                    name=name, 
                    phone=phone, 
                    message=message
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Сообщение отправлено! Мы свяжемся с вами в ближайшее время.'
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': 'Произошла ошибка при отправке сообщения'
                }, status=500)
        else:
            # Regular form submission
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            message = request.POST.get("message", "")
            session_key = request.POST.get("captcha_session_key")
            captcha_answer = request.POST.get("captcha_answer")
            
            # Validate CAPTCHA
            try:
                captcha_session = CaptchaSession.objects.get(session_key=session_key)
                if not captcha_session.is_solved and not captcha_session.verify_answer(captcha_answer):
                    # If CAPTCHA is invalid, redirect back to the form with an error
                    return render(request, "main/contacts.html", {
                        "error": "Неверный ответ CAPTCHA. Пожалуйста, попробуйте еще раз."
                    })
            except CaptchaSession.DoesNotExist:
                # If CAPTCHA session doesn't exist, redirect back to the form with an error
                return render(request, "main/contacts.html", {
                    "error": "Недействительная сессия CAPTCHA. Пожалуйста, попробуйте еще раз."
                })
            
            ContactRequest.objects.create(name=name, phone=phone, message=message)
            return render(request, "orders/contact_success.html")
    
    return redirect("contacts")
