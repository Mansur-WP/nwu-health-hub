from __future__ import annotations

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email="admin@nwu.com").exists():
    User.objects.create_superuser(
        email="maislformansur@gmail.com",
        password="Admin12345"
    )




class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(
        self, email: str, password: str | None, **extra_fields
    ):

        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str | None = None, **extra_fields
    ):

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email=email, password=password, **extra_fields)


    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)


        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True"
            )
        return self._create_user(email=email, password=password,
                                  **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        PATIENT = "patient", "Patient"
        DOCTOR = "doctor", "Doctor"
        PHARMACIST = "pharmacist", "Pharmacist"

    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.PATIENT
    )

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    def __str__(self) -> str:
        return f"{self.email} ({self.role})"

    @property
    def full_name(self) -> str:
        return " ".join([p for p in [self.first_name, self.last_name] if p]).strip()



