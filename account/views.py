from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.exceptions import TokenError


from django.contrib.auth import authenticate
import logging


from .utils import (
    get_tokens,
    handle_token_blacklist,
    set_token_max_age,
)

from .models import CustomUser


logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([AllowAny])
def handle_login(request):
    """api to handle login"""

    email = request.data.get("email")

    password = request.data.get("password")

    try:

        user = CustomUser.objects.get(email=email)

        if not user.is_superuser and not user.is_staff:

            raise exceptions.PermissionDenied("You are not authorised to login")

        authenticated_user = authenticate(email=email, password=password)

        if authenticated_user is None:

            raise exceptions.AuthenticationFailed("Your credentials did not match")

        tokens = get_tokens(authenticated_user)

        response = Response(
            {
                "message": "login successful",
                "user": {
                    "id": authenticated_user.id,
                    "isAdmin": authenticated_user.is_superuser,
                    "isStaff": authenticated_user.is_staff,
                    "lastLoggedIn": authenticated_user.last_login,
                },
            },
            status=status.HTTP_200_OK,
        )

        access_token_max_age, refresh_token_max_age = set_token_max_age()

        response.set_cookie(
            key="access",
            value=tokens["access"],
            max_age=access_token_max_age,
            secure=True,
            httponly=True,
            samesite="None",
        )

        response.set_cookie(
            key="refresh",
            value=tokens["refresh"],
            max_age=refresh_token_max_age,
            secure=True,
            httponly=True,
            samesite="None",
        )

        return response

    except CustomUser.DoesNotExist as e:

        logger.error(f"Error in account/views/handle_login: {e}")

        return Response(
            {"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    except exceptions.AuthenticationFailed as e:

        logger.error(f"Error in account/views/handle_login: {e}")

        return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    except exceptions.PermissionDenied as e:

        logger.error(f"Error in account/views/handle_login: {e}")

        return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    except Exception as e:

        logger.error(f"Error in account/views/handle_login: {e}")

        return Response(
            {"detail": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def check_logged_in_status(request):

    try:

        user = request.user

        is_logged_in = user.is_authenticated

        response_data = {
            "isLoggedIn": is_logged_in,
            "user": {
                "id": user.id,
                "isAdmin": user.is_superuser,
                "isStaff": user.is_staff,
                "lastLoggedIn": user.last_login if user.is_authenticated else None,
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except TokenError as e:

        logger.error(f"Error in account/views/check_logged_in_status: {e}")

        return Response(
            {"detail": "Invalid token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    except Exception as e:

        logger.error(f"Error in account/views/check_logged_in_status: {e}")

        print("Error in account/views/check_logged_in_status:", e)

        return Response(
            {"detail": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def handle_logout(request):
    try:

        refresh_token = request.COOKIES.get("refresh")

        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access",
            value="",
            max_age=0,
            secure=True,
            httponly=True,
            samesite="None",
        )
        response.set_cookie(
            key="refresh",
            value="",
            max_age=0,
            secure=True,
            httponly=True,
            samesite="None",
        )

        handle_token_blacklist(refresh_token)

        response["Authorization"] = ""

        return response

    except Exception as e:

        logger.error(f"Error in account/views/check_logged_in_status: {e}")

        return Response(
            {"detail": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
