from typing import Any

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


User = get_user_model()


def get_user(request: Any) -> Any:
    if not hasattr(request, "_cached_user"):
        request._cached_user = authenticate(request)
    return request._cached_user


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request: Any) -> None:
        def user():
            anonymous_user = AnonymousUser()
            return get_user(request) or anonymous_user

        request.user = SimpleLazyObject(func=lambda: user())
