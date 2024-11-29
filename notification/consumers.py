from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        if self.scope["user"].is_anonymous:
            logger.warning("Anonymous user attempted to connect")
            await self.close(code=4003)  # Authentication failed
            return

        try:

            self.user = self.scope["user"]
            self.room_group_name = f"notification_{self.user.id}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            logger.info(f"User {self.user.id} connected to notifications")
            await self.send(
                text_data=json.dumps(
                    {
                        "message": "Ready to send notifications",
                    }
                )
            )

        except Exception as e:
            logger.error(f"Error in connection setup: {str(e)}")
            await self.close(code=4000)  # Custom error code
            raise StopConsumer()

    async def disconnect(self, close_code):
        try:
            if hasattr(self, "room_group_name"):
                await self.channel_layer.group_discard(
                    self.room_group_name, self.channel_name
                )
                logger.info(f"User {self.user.id} disconnected from notifications")
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}")

        self.close(code=4000)
        raise StopConsumer()

    async def notification_message(self, event):

        await self.send(text_data=json.dumps(event["data"]))

        logger.info("Notification sent to user")


def send_notification_to_user(user_id, notification_data):
    channel_layer = get_channel_layer()
    group_name = f"notification_{user_id}"

    message = {"type": "notification_message", "data": notification_data}

    async_to_sync(channel_layer.group_send)(group_name, message)
