from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import *


urlpatterns = [
    path("robots.txt", robots_txt, name="robots_txt"),
path("sitemap.xml", sitemap_xml, name="sitemap_xml"),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('order/', include('orders.urls')),  
    path('services/', include('services.urls')), 
    path('captcha/', include('captcha.urls')),
    path('', include('main.urls')),              
]


handler404 = "main.views.custom_404"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
