# Generated by Django 5.2.1 on 2025-05-24 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Контент')),
                ('image', models.ImageField(blank=True, upload_to='about/', verbose_name='Изображение')),
                ('meta_description', models.TextField(blank=True, verbose_name='Meta Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'О компании',
                'verbose_name_plural': 'О компании',
            },
        ),
    ]
