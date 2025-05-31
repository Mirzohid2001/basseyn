from django.db import models

class ContactInfo(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()

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
    image = models.ImageField('Изображение', upload_to='banners/', blank=True)
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
