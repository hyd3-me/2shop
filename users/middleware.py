from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomJWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")

        if auth_header.startswith("Token "):
            token = auth_header[6:]
            request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
