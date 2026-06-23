from __future__ import annotations

from django.db import models

from accounts.models import User


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.user.full_name or self.user.email

