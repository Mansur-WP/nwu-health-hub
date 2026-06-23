from __future__ import annotations

from django import forms

from prescriptions.models import Prescription


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["medicine", "dosage", "instructions"]

    def save_with_appointment(self, appointment, created_by) -> Prescription:
        prescription = self.save(commit=False)
        prescription.appointment = appointment
        prescription.doctor = appointment.doctor
        prescription.patient = appointment.patient
        prescription.status = Prescription.Status.DRAFT
        prescription.save()
        return prescription

