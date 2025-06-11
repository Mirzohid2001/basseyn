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
                captcha_session_key = request.POST.get("captcha_session_key")
                
                # Validate required fields
                if not name or not phone:
                    return JsonResponse({
                        'success': False,
                        'error': 'Имя и телефон обязательны для заполнения'
                    }, status=400)
                    
                # Validate captcha
                if not captcha_session_key:
                    return JsonResponse({
                        'success': False,
                        'error': 'Необходимо пройти проверку CAPTCHA'
                    }, status=400)
                    
                # Check if captcha session exists and is verified
                try:
                    captcha_session = CaptchaSession.objects.get(session_key=captcha_session_key)
                    if not captcha_session.is_verified:
                        return JsonResponse({
                            'success': False,
                            'error': 'Проверка CAPTCHA не пройдена'
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
            captcha_session_key = request.POST.get("captcha_session_key")
            
            # Validate captcha
            if not captcha_session_key:
                return render(request, "orders/order_form.html", {
                    "products": products, 
                    "services": services,
                    "error": "Необходимо пройти проверку CAPTCHA"
                })
            
            # Check if captcha session exists and is verified
            try:
                captcha_session = CaptchaSession.objects.get(session_key=captcha_session_key)
                if not captcha_session.is_verified:
                    return render(request, "orders/order_form.html", {
                        "products": products, 
                        "services": services,
                        "error": "Проверка CAPTCHA не пройдена"
                    })
            except CaptchaSession.DoesNotExist:
                return render(request, "orders/order_form.html", {
                    "products": products, 
                    "services": services,
                    "error": "Недействительная сессия CAPTCHA"
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
                captcha_session_key = request.POST.get("captcha_session_key")
                
                # Validate required fields
                if not name or not phone:
                    return JsonResponse({
                        'success': False,
                        'error': 'Имя и телефон обязательны для заполнения'
                    }, status=400)
                    
                # Validate captcha
                if not captcha_session_key:
                    return JsonResponse({
                        'success': False,
                        'error': 'Необходимо пройти проверку CAPTCHA'
                    }, status=400)
                    
                # Check if captcha session exists and is verified
                try:
                    captcha_session = CaptchaSession.objects.get(session_key=captcha_session_key)
                    if not captcha_session.is_verified:
                        return JsonResponse({
                            'success': False,
                            'error': 'Проверка CAPTCHA не пройдена'
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
            captcha_session_key = request.POST.get("captcha_session_key")
            
            # Validate captcha
            if not captcha_session_key:
                return render(request, "main/contacts.html", {
                    "error": "Необходимо пройти проверку CAPTCHA"
                })
            
            # Check if captcha session exists and is verified
            try:
                captcha_session = CaptchaSession.objects.get(session_key=captcha_session_key)
                if not captcha_session.is_verified:
                    return render(request, "main/contacts.html", {
                        "error": "Проверка CAPTCHA не пройдена"
                    })
            except CaptchaSession.DoesNotExist:
                return render(request, "main/contacts.html", {
                    "error": "Недействительная сессия CAPTCHA"
                })
                
            ContactRequest.objects.create(name=name, phone=phone, message=message)
            return render(request, "orders/contact_success.html")
    
    return redirect("contacts")
