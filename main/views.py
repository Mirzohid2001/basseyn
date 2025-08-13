# main/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import InfoPage, ContactInfo, About, Banner, Projectt
from products.models import Category
from django.template.loader import render_to_string
from django.http import HttpResponse

def home(request):
    # Получаем категории с количеством товаров
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)[:6]  # Берем только категории с товарами, максимум 6
    
    # Получаем активные баннеры
    banners = Banner.objects.filter(is_active=True)
    contact = ContactInfo.objects.first()
    projects = Projectt.objects.filter(is_active=True).order_by("order", "-created_at")


    context = {
        'categories': categories,
        'banners': banners,
        'contact':contact,
        "projects": projects
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

def robots_txt(request):
    text = render_to_string('robots.txt')  # если в templates/robots.txt
    return HttpResponse(text, content_type="text/plain")


def sitemap_xml(request):
    text = render_to_string('sitemap.xml')
    return HttpResponse(text, content_type="application/xml")
