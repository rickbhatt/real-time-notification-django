from django.urls import path

from . import views


urlpatterns = [
    path(
        "get-unread-notifications/",
        views.get_unread_notifications,
        name="get-unread-notifications",
    ),
    path(
        "mark-notification-as-read/",
        views.mark_notification_as_read,
    ),
]
