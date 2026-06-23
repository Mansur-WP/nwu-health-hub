from __future__ import annotations

from django.db import models

from accounts.models import User
from doctors.models import DoctorProfile
from patients.models import PatientProfile


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        CANCELLED = "cancelled", "Cancelled"

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return (
            f"Appointment({self.patient.user.email} - {self.doctor.user.email})"
        )


