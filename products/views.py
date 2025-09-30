# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.template.loader import render_to_string

from main.models import SEOSettings
from .models import Product, Category


def _seo_from_settings(page_name: str):
    try:
        s = SEOSettings.objects.get(page_name=page_name)
        return {"title": s.title or None, "description": s.description or None, "canonical": s.canonical or None}
    except SEOSettings.DoesNotExist:
        return {"title": None, "description": None, "canonical": None}

def _canonical_base(request):
    # каноникал без параметров
    return request.build_absolute_uri(request.path)

def product_list(request):
    products = Product.objects.select_related("category").prefetch_related("images").all()
    categories = Category.objects.all()

    q = request.GET.get("q", "")
    category = request.GET.get("category", "")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if category:
        products = products.filter(category__id=category)
    if min_price:
        try: products = products.filter(price__gte=float(min_price))
        except ValueError: pass
    if max_price:
        try: products = products.filter(price__lte=float(max_price))
        except ValueError: pass

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

    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # SEO для списка
    ss = _seo_from_settings("product_list")
    seo_title = ss["title"] or "Каталог товаров — Водопадов"
    seo_description = ss["description"] or "Каталог продукции для бассейнов: оборудование, химия, аксессуары."
    base_canon = ss["canonical"] or _canonical_base(request)
    seo_canonical = f"{base_canon}?page={page_obj.number}" if page_obj.number > 1 else base_canon

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
        # SEO
        "seo_title": seo_title,
        "seo_description": seo_description,
        "seo_canonical": seo_canonical,
    }

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


# === НОВОЕ: детальная по SLUG ===
def product_detail_by_slug(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("images", "characteristics"),
        slug=slug
    )
    # твой существующий SEO-код можно переиспользовать
    return render(request, "products/product_detail.html", {"product": product})


# === ЛЕГАСИ: детальная по ID с 301-редиректом на slug ===
def product_detail_legacy(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if not product.slug:
        product.slug = str(product.pk)
        product.save(update_fields=['slug'])
    from django.shortcuts import redirect
    return redirect(product.get_absolute_url(), permanent=True)

