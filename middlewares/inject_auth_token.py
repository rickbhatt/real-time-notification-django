from rest_framework_simplejwt.exceptions import TokenError
import logging

from .utils import handle_token_rotation, validate_access_token

from account.utils import set_token_max_age


logger = logging.getLogger(__name__)


class InjectAuthTokenMiddleware:
    """
    middleware to inject and handle access and refresh tokens
    in the header of the request
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        access_token = request.COOKIES.get("access")

        refresh_token = request.COOKIES.get("refresh")

        exclude_paths = ["/api/v2/account/logout/"]

        # the user is not authenticated or not logged in
        try:

            if request.path in exclude_paths:

                return self.get_response(request)

            if access_token:
                # Attempt to validate the access token
                valid_token = validate_access_token(access_token)

                if valid_token:

                    # If successful, set the Authorization header
                    request.META["HTTP_AUTHORIZATION"] = f"Bearer {valid_token}"
                else:

                    access_token = None

            if not access_token and refresh_token:

                # if refresh token is present but not access token then the access token
                # is expired
                # token rotation takes place

                try:

                    tokens = handle_token_rotation(refresh_token)

                    new_access_token = tokens["access"]
                    new_refresh_token = tokens["refresh"]

                    request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access_token}"

                    # Get the response

                    response = self.get_response(request)

                    access_token_max_age, refresh_token_max_age = set_token_max_age()

                    # Set the new access token cookie
                    response.set_cookie(
                        key="access",
                        value=new_access_token,
                        max_age=access_token_max_age,
                        secure=True,
                        httponly=True,
                        samesite="None",
                    )

                    response.set_cookie(
                        key="refresh",
                        value=new_refresh_token,
                        max_age=refresh_token_max_age,
                        secure=True,
                        httponly=True,
                        samesite="None",
                    )

                    return response

                except TokenError:
                    logger.error("Token rotation failed")

                    # Optionally, clear the invalid refresh token
                    response = self.get_response(request)
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
                    return response

            return self.get_response(request)

        except Exception as e:

            logger.error(f"Error in InjectAuthTokenMiddleware: {str(e)}")

            return self.get_response(request)
