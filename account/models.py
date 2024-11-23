from django.db import models

import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager, ActiveUsersManager


class AllBoolChecks(models.Model):
    is_suspended = models.BooleanField(default=False)

    is_payment_defaulter = models.BooleanField(default=False)

    is_profile_available = models.BooleanField(default=False)

    class Meta:
        abstract = True


class CustomUser(AbstractBaseUser, PermissionsMixin, AllBoolChecks):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    email = models.EmailField(unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    last_logged_out = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    active_objects = ActiveUsersManager()

    USERNAME_FIELD = "email"

    class Meta:
        managed = False

    def __str__(self):
        return f"{self.email} | {self.id}"
