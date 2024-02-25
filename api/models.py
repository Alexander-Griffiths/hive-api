from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
import uuid

class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('You must provide an username')
        user = self.model(username=username, **extra_fields)
        if password is None:
            user.set_unusable_password()
        else:   
            user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        user = self.create_user(email, password, **extra_fields)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    # Essentials
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, null=True)
    # Time related
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    # Properties
    verified = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_robot = models.BooleanField(default=False)

    USERNAME_FIELD = 'userrname'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ("-created_at",)