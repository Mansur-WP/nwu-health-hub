from __future__ import annotations

from django.db import models
from django.utils import timezone

from doctors.models import DoctorProfile
from patients.models import PatientProfile


class Prescription(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending"
        DISPENSED = "dispensed", "Dispensed"

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    appointment = models.OneToOneField(
        "appointments.Appointment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="prescription",
    )

    medicine = models.CharField(max_length=200)
    dosage = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)

    date = models.DateField(default=timezone.now)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return f"Prescription({self.medicine} - {self.patient.user.email})"
