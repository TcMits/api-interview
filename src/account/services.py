from typing import Any

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def login(instance: User, request: Any = None) -> User:
    # TODO: something
    instance.last_login = timezone.now()
    instance.save(update_fields=["last_login"])
    return instance
