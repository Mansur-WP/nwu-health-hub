from __future__ import annotations

from decimal import Decimal

from django.db import models

from accounts.models import User
from appointments.models import Appointment
from patients.models import PatientProfile


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Payment({self.appointment_id} - {self.status})"

