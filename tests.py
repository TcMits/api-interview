from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from src.core.jwt import create_access_token

User = get_user_model()


class TestApiInterview(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.authenticated_user = User.objects.create_superuser(
            email="test@gmail.com",
            username="testinterview",
            password="12345678",
            last_name="test",
            first_name="test",
        )

    def test_login_api(self):
        url = reverse("login")
        verify_url = reverse("verify-token")

        resp = self.client.post(
            url, {"username": self.authenticated_user.username, "password": "12345678"}
        )

        resp_json = resp.json()
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(verify_url, {"token": resp_json["token"]})
        self.assertEqual(resp.status_code, 200)

    def test_login_and_invalidate_old_token_api(self):
        url = reverse("login")
        verify_url = reverse("verify-token")

        resp = self.client.post(
            url, {"username": self.authenticated_user.username, "password": "12345678"}
        )

        self.assertEqual(resp.status_code, 200)
        old_token = resp.json()["token"]

        resp = self.client.post(
            url, {"username": self.authenticated_user.username, "password": "12345678"}
        )
        self.assertEqual(resp.status_code, 200)
        new_token = resp.json()["token"]

        resp = self.client.post(verify_url, {"token": new_token})
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(verify_url, {"token": old_token})
        self.assertEqual(resp.status_code, 401)

    def test_me_api(self):
        url = reverse("me")
        token = create_access_token(self.authenticated_user)

        resp = self.client.get(url, HTTP_AUTHORIZATION="JWT " + token)

        resp_json = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_json["is_active"], self.authenticated_user.is_active)
        self.assertEqual(resp_json["email"], self.authenticated_user.email)
        self.assertEqual(
            resp_json["name"],
            self.authenticated_user.last_name
            + " "
            + self.authenticated_user.first_name,
        )
