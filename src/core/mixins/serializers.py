from typing import (
    Any,
)

from rest_framework import serializers
from django.conf import settings
from django.utils.functional import classproperty


class GetRequestSerializerMixin:
    def get_request(self):
        return self.context.get("request")

    @property
    def request(self):
        return self.get_request()


class GetViewSerializerMixin:
    def get_view(self):
        return self.context.get("view")

    @property
    def view(self):
        return self.get_view()


class ViewProxySerializerMixin(GetRequestSerializerMixin):
    _view_serializer_instance = None
    _as_action: bool = False

    view_serializer = None
    many_through_view_serializer: bool = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._as_action = kwargs.pop("as_action", False)

        super().__init__(*args, **kwargs)
        if self.is_proxy:
            self._view_serializer_instance = self.view_serializer(*args, **kwargs)
        elif settings.FORCE_PROXY_SERIALIZER:
            raise

    @classproperty
    def is_proxy(cls) -> bool:
        return cls.view_serializer is not None

    @classmethod
    def many_init(cls, *args, **kwargs):  # noqa: ANN001,ANN002
        if cls.many_through_view_serializer and cls.is_proxy:
            return cls.view_serializer.many_init(*args, **kwargs)
        return super().many_init(*args, **kwargs)

    def bind(self, field_name: str, parent: serializers.Serializer) -> None:
        result = super().bind(field_name, parent)
        if self.is_proxy:
            self._view_serializer_instance.bind(
                field_name,
                parent
                if not getattr(parent, "is_proxy", False)
                else parent._view_serializer_instance,
            )
        return result

    def to_representation(self, instance: Any):
        request = self.request
        if not request:
            return super().to_representation(instance)

        if not self._as_action and self.is_proxy and instance:
            return self._view_serializer_instance.to_representation(instance)
        return super().to_representation(instance)
