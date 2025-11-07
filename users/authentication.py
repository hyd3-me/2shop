import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions, HTTP_HEADER_ENCODING

User = get_user_model()


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get("HTTP_AUTHORIZATION", b"")
    if isinstance(auth, str):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class CustomJWTAuthentication(authentication.BaseAuthentication):

    keyword = "Token"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            jwt_token = auth[1].decode()
        except UnicodeError:
            msg = _(
                "Invalid token header. Token string should not contain invalid characters."
            )
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(jwt_token)

    def authenticate_credentials(self, jwt_token):
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            if not user_id:
                raise exceptions.AuthenticationFailed("Invalid token payload.")

            user = User.objects.get(pk=user_id)

            if not user.is_active:
                raise exceptions.AuthenticationFailed("User inactive or deleted.")

            return (user, jwt_token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired.")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token.")
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found.")

    def authenticate_header(self, request):
        return self.keyword
