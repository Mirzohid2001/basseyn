from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@receiver(post_save, sender=Order)
def notify_admin_on_order(sender, instance, created, **kwargs):
    if created:
        subject = "Новый заказ на сайте"
        product_info = f"\nТовар: {instance.product}" if instance.product else ""
        service_info = f"\nУслуга: {instance.service}" if instance.service else ""
        message = (
            f"Имя: {instance.client_name}\n"
            f"Телефон: {instance.client_phone}{product_info}{service_info}\n"
            f"Комментарий: {instance.comment}\n"
            f"Дата: {instance.created_at.strftime('%Y-%m-%d %H:%M')}"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.NOTIFY_EMAIL],  # Можно несколько адресов: ['...', '...']
            fail_silently=False,
        )
