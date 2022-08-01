from typing import Any

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from src.api.serializers.login import (
    LoginActionSerializer,
    MeViewSerializer,
    VerifyTokenSerializer,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin

User = get_user_model()


class LoginView(GenericViewSet):

    serializer_class = LoginActionSerializer
    permission_classes = [AllowAny]

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        ser = self.get_serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(
                ser.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": _("xác minh thất bại")}, status=status.HTTP_401_UNAUTHORIZED
        )


class VerifyTokenView(GenericViewSet):

    serializer_class = VerifyTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        ser = self.get_serializer(data=request.data)
        if not ser.is_valid():
            return Response(
                {"message": _("xác minh thất bại")}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(status=status.HTTP_200_OK)


class MeViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = MeViewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user
