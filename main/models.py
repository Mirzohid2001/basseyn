from django.db import models

class ContactInfo(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    telegram = models.CharField(max_length=100)

    def __str__(self):
        return self.address

class InfoPage(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class About(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Контент')
    image = models.ImageField('Изображение', upload_to='about/', blank=True)
    meta_description = models.TextField('Meta Description', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'О компании'
        verbose_name_plural = 'О компании'

class Banner(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.TextField('Подзаголовок', blank=True)
    link = models.CharField('Ссылка', max_length=255, blank=True)
    link_text = models.CharField('Текст кнопки', max_length=100, blank=True, default='Подробнее')
    background_color = models.CharField('Цвет фона', max_length=20, blank=True, help_text='Например: #0099cc или rgba(0,153,204,0.9)')
    is_active = models.BooleanField('Активен', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рекламный баннер'
        verbose_name_plural = 'Рекламные баннеры'
        ordering = ['order', '-created_at']

class BannerImage(models.Model):
    banner = models.ForeignKey(
        'Banner', related_name='images', on_delete=models.CASCADE, verbose_name='Баннер'
    )
    image = models.ImageField('Изображение', upload_to='banner_images/')
    alt_text = models.CharField('Альтернативный текст', max_length=120, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    def __str__(self):
        return f"Изображение для {self.banner.title}"

    class Meta:
        verbose_name = 'Изображение баннера'
        verbose_name_plural = 'Изображения баннеров'
        ordering = ['order', 'id']

class SEOSettings(models.Model):
    page_name = models.CharField(
        "URL name страницы",
        max_length=100,
        unique=True,
        help_text="Имя маршрута (url_name) из urls.py. Например: home, product_list, product_detail, service_list, service_detail, contacts"
    )
    title = models.CharField("Title", max_length=255, blank=True,
                             help_text="Заголовок страницы (<title>)")
    description = models.TextField("Meta description", blank=True,
                                   help_text="Описание страницы (meta description)")
    canonical = models.URLField("Canonical URL", blank=True,
                                help_text="Каноническая ссылка на страницу")

    class Meta:
        verbose_name = "SEO-настройка"
        verbose_name_plural = "SEO-настройки"

    def __str__(self):
        return f"{self.page_name} — {self.title or 'Без title'}"

class Projectt(models.Model):
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Фоновое фото", upload_to="projects/")
    is_active = models.BooleanField("Показывать на сайте", default=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title