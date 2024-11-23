from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import logging

logger = logging.getLogger(__name__)

def validate_access_token(access_token_string):

    try:
        AccessToken(access_token_string)
        return access_token_string
    except TokenError:
        logger.error("Invalid access token")
        return None


def handle_token_rotation(refresh_token):

    try:

        refresh = RefreshToken(refresh_token)

        refresh_token = str(refresh)

        access_token = str(refresh.access_token)

        tokens = {"refresh": refresh_token, "access": access_token}

        return tokens

    except TokenError:
        
        logger.error("Invalid refresh token in the middleware")

        raise TokenError("Invalid refresh token")
