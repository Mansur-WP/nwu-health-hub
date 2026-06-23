from __future__ import annotations

from django.db import models

from accounts.models import User


class PharmacistProfile(models.Model):
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

    phone = models.CharField(max_length=30, blank=True)


    def __str__(self) -> str:
        return f"PharmacistProfile({self.user.email})"


class MedicationInventory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Stock: {self.stock_quantity})"

