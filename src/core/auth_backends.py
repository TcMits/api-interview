from typing import Any, Optional, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend as DjangoModelBackend
from jwt import PyJWTError

from src.core.jwt import get_token_from_request, get_user_from_access_token

User = get_user_model()


def get_user(user_id: Union[int, str]) -> User:
    user_id = str(user_id)
    if user_id.isnumeric():
        return User.objects.get(id=user_id, is_active=True)
    return User.objects.get(username=user_id, is_active=True)


class ModelBackend(DjangoModelBackend):
    def authenticate(
        self,
        request: Any,
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any
    ) -> Optional[User]:
        if username is None:
            username = kwargs.get("email")

        if username is None:
            username = kwargs.get("main_phone_number")

        if username is None or password is None or not request:
            return None
        try:
            user = self.get_user(username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id: Union[str, int]) -> User:
        return get_user(user_id)


class JSONWebTokenBackend(DjangoModelBackend):
    def authenticate(self, request: Any, **kwargs: Any) -> Optional[User]:
        if not request:
            return None

        token = get_token_from_request(request)
        if not token:
            return None
        try:
            user = get_user_from_access_token(token)
        except PyJWTError:
            return None
        return user

    def get_user(self, user_id: Union[str, int]) -> User:
        return get_user(user_id)
