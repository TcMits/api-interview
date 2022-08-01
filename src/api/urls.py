from django.urls import path

from src.api.views.login import LoginView, MeViewSet, VerifyTokenView

urlpatterns = [
    path("login/", LoginView.as_view({"post": "post"}), name="login"),
    path(
        "verify-token/", VerifyTokenView.as_view({"post": "post"}), name="verify-token"
    ),
    path("me/", MeViewSet.as_view({"get": "retrieve"}), name="me"),
]
