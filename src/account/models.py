from django.utils.translation import gettext_lazy as _
from django.contrib.auth import models as auth_models
from typing import Any, Optional


class UserManager(auth_models.BaseUserManager):
    def create_user(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        is_active: bool = True,
        **extra_fields: Any
    ) -> "User":
        if not username:
            raise ValueError("The given username must be set")
        if email:
            email = UserManager.normalize_email(email)
        user = self.model(
            username=username,
            is_active=is_active,
            **extra_fields,
        )
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields: Any) -> "User":
        extra_fields.update({"is_staff": True, "is_active": True, "is_superuser": True})
        return self.create_user(
            **extra_fields,
        )


class User(auth_models.AbstractUser):
    # TODO: something

    class Meta:
        verbose_name = _("Tài khoản")
        verbose_name_plural = _("Tài khoản")
        app_label = "account"
