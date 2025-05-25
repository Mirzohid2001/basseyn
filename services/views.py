# services/views.py
from django.shortcuts import render, get_object_or_404
from .models import Service, Project

def service_list(request):
    services = Service.objects.prefetch_related("images").all()
    q = request.GET.get("q", "")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort", "")
    if q:
        services = services.filter(name__icontains=q)
    if min_price:
        services = services.filter(price__gte=min_price)
    if max_price:
        services = services.filter(price__lte=max_price)
    if sort == "price_asc":
        services = services.order_by("price")
    elif sort == "price_desc":
        services = services.order_by("-price")
    else:
        services = services.order_by("id")
    return render(request, "services/service_list.html", {
        "services": services,
        "q": q,
        "min_price": min_price or "",
        "max_price": max_price or "",
        "sort": sort,
    })

def service_detail(request, pk):
    service = get_object_or_404(Service.objects.prefetch_related("images"), pk=pk)
    return render(request, "services/service_detail.html", {"service": service})

def project_list(request):
    projects = Project.objects.prefetch_related("images").all()
    q = request.GET.get("q", "")
    if q:
        projects = projects.filter(title__icontains=q)
    return render(request, "services/project_list.html", {"projects": projects, "q": q})

def project_detail(request, pk):
    project = get_object_or_404(Project.objects.prefetch_related("images"), pk=pk)
    return render(request, "services/project_detail.html", {"project": project})
