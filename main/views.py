# main/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import InfoPage, ContactInfo, About
from products.models import Category

def home(request):
    # Получаем категории с количеством товаров
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)[:6]  # Берем только категории с товарами, максимум 6
    
    context = {
        'categories': categories
    }
    return render(request, "main/home.html", context)

def contacts(request):
    info = ContactInfo.objects.first()
    return render(request, "main/contacts.html", {"contact": info})

def info_page(request, slug):
    page = get_object_or_404(InfoPage, slug=slug, is_active=True)
    return render(request, "main/info_page.html", {"page": page})

def faq(request):
    return render(request, "main/faq.html")

def custom_404(request, exception):
    return render(request, "404.html", status=404)

def about_view(request):
    about = About.objects.first()
    return render(request, 'main/about.html', {
        'about': about
    })
