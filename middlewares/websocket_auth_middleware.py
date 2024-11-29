from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
import logging


logger = logging.getLogger(__name__)


class WebsocketAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):

        headers = dict(scope["headers"])

        cookie_header = headers.get(b"cookie").decode()

        # Parse cookies
        cookies = {}

        if cookie_header:
            cookies = {
                cookie.split("=")[0].strip(): cookie.split("=")[1].strip()
                for cookie in cookie_header.split(";")
                if "=" in cookie
            }

        refresh_token = cookies.get("refresh")

        try:

            if not refresh_token:

                scope["user"] = AnonymousUser()
                return await super().__call__(scope, receive, send)

            user = await self.get_user_from_token(refresh_token)

            if not user.is_authenticated:
                scope["user"] = AnonymousUser()
                return await super().__call__(scope, receive, send)

            scope["user"] = user
            scope["refresh_token"] = refresh_token

            return await super().__call__(scope, receive, send)

        except Exception as e:
            logger.error(f"Critical error in WebSocket middleware: {str(e)}")
            scope["user"] = AnonymousUser()
            return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):

        user = None

        try:

            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            User = get_user_model()

            user = User.objects.get(id=decoded_token["user_id"])

            return user

        except jwt.ExpiredSignatureError:
            logger.warning("Expired refresh token in WebSocket connection")
            return user

        except jwt.InvalidTokenError:
            logger.warning("Invalid refresh token in WebSocket connection")
            return user
