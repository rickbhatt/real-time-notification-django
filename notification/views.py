from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_unread_notifications(request):

    try:

        user = request.user

        objs = Notification.objects.filter(
            recipient=user, status=Notification.Status.UNREAD
        )
        serializer = NotificationSerializer(objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in notification/views/get_unread_notifications: {e}")
        return Response(
            {"detail": "Internal Server Error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
