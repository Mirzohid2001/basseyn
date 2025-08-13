from .models import SEOSettings

def seo_context(request):
    """
    Добавляет в контекст: seo_title, seo_description, seo_canonical
    по текущему имени маршрута (url_name).
    """
    match = getattr(request, "resolver_match", None)
    if not match:
        return {}

    page_name = match.url_name
    data = {
        "seo_title": None,
        "seo_description": None,
        "seo_canonical": request.build_absolute_uri(request.path),  # дефолт
    }
    try:
        s = SEOSettings.objects.get(page_name=page_name)
        if s.title:
            data["seo_title"] = s.title
        if s.description:
            data["seo_description"] = s.description
        if s.canonical:
            data["seo_canonical"] = s.canonical
    except SEOSettings.DoesNotExist:
        pass
    return data
