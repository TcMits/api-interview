from typing import Any, Union

from django.contrib.auth import authenticate, get_user_model
from django.http import QueryDict
from django.middleware.csrf import (
    _get_new_csrf_string,
    _mask_cipher_secret,
)
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from rest_framework import exceptions

from jwt.exceptions import PyJWTError
from rest_framework import serializers

from src.account.services import login
from src.core.jwt import (
    create_access_token,
    create_refresh_token,
    get_user_from_access_token,
)
from src.core.mixins.serializers import ViewProxySerializerMixin

User = get_user_model()


class LoginViewSerializer(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()
    csrf_token = serializers.SerializerMethodField()

    @cached_property
    def __csrf_token(self) -> str:
        return _mask_cipher_secret(_get_new_csrf_string())

    def get_csrf_token(self, __: User) -> str:
        return self.__csrf_token

    def get_refresh_token(self, obj: User) -> str:
        return create_refresh_token(obj, {"csrf_token": self.__csrf_token})

    def get_token(self, obj: User) -> str:
        return create_access_token(obj)

    class Meta:
        model = User
        fields = (
            "token",
            "refresh_token",
            "csrf_token",
        )


class LoginActionSerializer(ViewProxySerializerMixin, serializers.Serializer):
    view_serializer = LoginViewSerializer

    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(
        max_length=128,
        required=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs: Union[dict, QueryDict]) -> Union[dict, QueryDict]:
        assert not self.instance
        request = self.context["request"]
        user = authenticate(
            request=request, username=attrs["username"], password=attrs["password"]
        )
        if not user:
            raise serializers.ValidationError(_("%s không hợp lệ") % (_("Tài khoản"),))
        self.instance = user
        return attrs

    def save(self, **kwargs: Any) -> User:
        request = self.request
        self.instance = login(self.instance, request)
        if hasattr(request, "_request"):
            request._request._cached_user = self.instance
        return self.instance


class VerifyTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, allow_null=False)

    def validate(self, attrs: Union[dict, QueryDict]) -> Union[dict, QueryDict]:
        attrs = super().validate(attrs)
        try:
            get_user_from_access_token(attrs["token"])
        except PyJWTError:
            raise exceptions.ValidationError(_("%s không hợp lệ") % (_("Mã"),))
        return attrs


class MeViewSerializer(serializers.Serializer):
    # TODO: something
    pass
