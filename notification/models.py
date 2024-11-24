from django.db import models
from django.conf import settings

from django.utils import timezone


class Notification(models.Model):
    """
    A simple notification model for tracking user notifications
    """

    class Status(models.TextChoices):
        UNREAD = "unread", ("Unread")
        READ = "read", ("Read")

    # Core fields
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=("Recipient"),
    )
    title = models.CharField(max_length=255, verbose_name=("Title"))
    message = models.TextField(verbose_name=("Message"))
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.UNREAD,
        verbose_name=("Status"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("Created At"))
    read_at = models.DateTimeField(null=True, blank=True, verbose_name=("Read At"))

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.recipient}: {self.title}"

    def mark_as_read(self):
        """Mark the notification as read"""
        if self.status == self.Status.UNREAD:
            self.status = self.Status.READ
            self.read_at = timezone.now()
            self.save(update_fields=["status", "read_at"])

    def mark_as_unread(self):
        """Mark the notification as unread"""
        self.status = self.Status.UNREAD
        self.read_at = None
        self.save(update_fields=["status", "read_at"])
