from typing import Any, Tuple

from rest_framework import authentication


class APIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Any) -> Tuple[Any, None]:
        user = getattr(request._request, "user", None)
        return (user, None)
