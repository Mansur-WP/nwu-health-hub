from __future__ import annotations

from django.db import models

from accounts.models import User


class DoctorProfile(models.Model):
    class ApprovalStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    approval_status = models.CharField(
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
    )
    approval_note = models.TextField(blank=True)

    specialization = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=30, blank=True)


    def __str__(self) -> str:
        name = self.user.full_name or self.user.email
        spec = f" — {self.specialization}" if self.specialization else ""
        return f"Dr. {name}{spec}"


