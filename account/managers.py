from django.contrib.auth.base_user import BaseUserManager

from django.utils.translation import gettext_lazy as _

from django.db.models import QuerySet
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(_("is staff must be set to true"))

        if other_fields.get("is_superuser") is not True:
            raise ValueError(_("is superuser must be set to true"))

        return self.create_user(email, password, **other_fields)

    def create_staff(self, email, password, **other_fields):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError(_("is staff must be set to true"))

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_("The email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class ActiveUsersManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_active=True)
