# orders/views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseGone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Order, ContactRequest
from products.models import Product
from services.models import Service
from captcha.models import CaptchaSession
import json

def order_create(request):
    if request.method == "GET" and "product" in request.GET:
        resp = HttpResponseGone("Старая страница заказа удалена")
        resp["X-Robots-Tag"] = "noindex, nofollow"
        return resp
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


from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from products.models import Product
from .cart import Cart
from .models import Order, OrderItem

@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get("qty", 1))
    replace = request.POST.get("replace") == "1"
    cart = Cart(request)
    cart.add(product_id=product.id, qty=qty, replace=replace)
    return redirect("cart_detail")

def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect("cart_detail")

@require_POST
def cart_update(request, product_id):
    qty = int(request.POST.get("qty", 1))
    cart = Cart(request)
    cart.add(product_id, qty=qty, replace=True)
    return redirect("cart_detail")

def cart_detail(request):
    cart = Cart(request)
    return render(request, "orders/cart_detail.html", {"cart": cart})

def checkout(request):
    cart = Cart(request)
    if cart.total_qty() == 0:
        return redirect("cart_detail")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        comment = request.POST.get("comment", "").strip()

        if not name or not phone:
            return render(request, "orders/checkout.html", {"cart": cart, "error": "Укажите имя и телефон."})

        order = Order.objects.create(
            client_name=name,
            client_phone=phone,
            client_email=email or "",
            comment=comment or "",
            status="new",
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["qty"],
                price_at_time=item["price"],
            )

        # письмо админу
        lines = [
            f"Новый заказ #{order.id}",
            f"Имя: {order.client_name}",
            f"Телефон: {order.client_phone}",
            f"Почта: {order.client_email or '—'}",
            f"Комментарий: {order.comment or '—'}",
            "",
            "Состав заказа:",
        ]
        for it in order.items.select_related("product"):
            lines.append(f"- {it.product.name} × {it.quantity} = {it.line_total()} ₽")
        lines.append("")
        lines.append(f"Итого: {cart.total_price()} ₽")

        send_mail(
            subject=f"Новый заказ #{order.id}",
            message="\n".join(lines),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[getattr(settings, "NOTIFY_EMAIL", settings.DEFAULT_FROM_EMAIL)],
            fail_silently=False,
        )

        # Сохраняем данные для «Мои заказы»
        request.session["last_order_id"] = order.id
        request.session["order_lookup"] = {"phone": phone, "email": email}

        cart.clear()
        return redirect("checkout_success")

    return render(request, "orders/checkout.html", {"cart": cart})

def checkout_success(request):
    order_id = request.session.get("last_order_id")
    phone = (request.session.get("order_lookup") or {}).get("phone")
    email = (request.session.get("order_lookup") or {}).get("email")
    order = None
    if order_id:
        order = Order.objects.filter(id=order_id).prefetch_related("items__product").first()
    return render(request, "orders/checkout_success.html", {
        "order": order,
        "phone": phone,
        "email": email,
    })

# ===== Мои заказы =====

def my_orders(request):
    """Показывает список заказов по телефону/почте из сессии или предлагает форму поиска."""
    lookup = request.session.get("order_lookup") or {}
    phone = (lookup.get("phone") or "").strip()
    email = (lookup.get("email") or "").strip()

    orders = []
    if phone or email:
        qs = Order.objects.all()
        if phone:
            qs = qs.filter(client_phone=phone)
        if email:
            qs = qs.filter(client_email=email)
        orders = (qs.order_by("-created_at")
                    .prefetch_related("items__product"))

    return render(request, "orders/my_orders.html", {
        "orders": orders,
        "phone": phone,
        "email": email,
    })

@require_POST
def my_orders_set_lookup(request):
    """Сохраняет телефон/почту в сессию и кидает на список заказов."""
    phone = request.POST.get("phone", "").strip()
    email = request.POST.get("email", "").strip()
    if not phone and not email:
        messages.error(request, "Укажите телефон или почту.")
        return redirect("my_orders")
    request.session["order_lookup"] = {"phone": phone, "email": email}
    return redirect("my_orders")

def order_detail(request, pk: int):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"), pk=pk
    )
    lookup = request.session.get("order_lookup") or {}
    phone = (lookup.get("phone") or "").strip()
    email = (lookup.get("email") or "").strip()

    allowed = (phone and order.client_phone == phone) or (
        email and order.client_email and order.client_email == email
    )
    if not allowed:
        messages.error(request, "Для просмотра заказа укажите телефон/почту, использованные при оформлении.")
        return redirect("my_orders")

    # Считаем итог на стороне сервера и передаём в шаблон
    order_total = sum((it.line_total() for it in order.items.all()), 0)
    return render(request, "orders/order_detail.html", {
        "order": order,
        "order_total": order_total,
    })

