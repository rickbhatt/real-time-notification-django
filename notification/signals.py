from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Notification


@receiver(post_save, sender=Notification)
def send_push_notification(sender, instance, created, **kwargs):

    if created:
        print("Notification created")
