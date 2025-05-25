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
