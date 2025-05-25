# products/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Product, Category

def product_list(request):
    products = Product.objects.select_related("category").prefetch_related("images").all()
    categories = Category.objects.all()
    
    # Filter parameters
    q = request.GET.get("q", "")
    category = request.GET.get("category", "")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    
    # Apply filters
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if category:
        products = products.filter(category__id=category)
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Sorting
    sort = request.GET.get("sort", "")
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "date_new":
        products = products.order_by("-id")
    elif sort == "date_old":
        products = products.order_by("id")
    elif sort == "popular":
        products = products.annotate(order_count=Count("order")).order_by("-order_count")
    else:
        products = products.order_by("-id")
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page for better grid layout
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "products": page_obj,
        "categories": categories,
        "current_category": category,
        "q": q,
        "min_price": min_price or "",
        "max_price": max_price or "",
        "sort": sort,
        "paginator": paginator,
        "page_obj": page_obj,
    }
    
    # AJAX request - return only the product grid
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('products/product_grid_partial.html', context, request=request)
        return JsonResponse({
            'success': True,
            'html': html,
            'total_count': paginator.count,
            'page_count': paginator.num_pages,
            'current_page': page_obj.number,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous()
        })
    
    return render(request, "products/product_list.html", context)

def product_detail(request, pk):
    product = get_object_or_404(Product.objects.prefetch_related("images"), pk=pk)
    
    # Related products
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=product.pk).prefetch_related("images")[:4]
    
    context = {
        "product": product,
        "related_products": related_products
    }
    
    return render(request, "products/product_detail.html", context)
