from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.utils import timezone


def get_tokens(user):

    try:
        refresh = RefreshToken.for_user(user)

        tokens = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return tokens

    except Exception as e:
        raise e


def set_token_expiration():

    access_token_exp = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] + timezone.now()

    refresh_token_exp = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] + timezone.now()

    return access_token_exp, refresh_token_exp


def set_token_max_age():

    access_token_max_age = int(
        settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
    )

    refresh_token_max_age = int(
        settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
    )

    # print(access_token_max_age, refresh_token_max_age)

    return access_token_max_age, refresh_token_max_age


def handle_token_blacklist(refresh_token):

    try:
        token = RefreshToken(refresh_token)

        token.blacklist()
    except Exception as e:

        raise e
