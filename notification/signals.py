from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from .consumers import send_notification_to_user


@receiver(post_save, sender=Notification)
def send_push_notification(sender, instance, created, **kwargs):

    if created:

        notification_data = {
            "title": instance.title,
            "message": instance.message,
            "status": instance.status,
            "created_at": str(instance.created_at),
        }

        send_notification_to_user(instance.recipient.id, notification_data)
