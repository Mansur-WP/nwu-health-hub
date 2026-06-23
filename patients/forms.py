from __future__ import annotations

from django import forms

from appointments.models import Appointment
from doctors.models import DoctorProfile
from patients.models import PatientProfile


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ["phone", "address"]


class BookAppointmentForm(forms.Form):
    doctor = forms.ModelChoiceField(
        queryset=DoctorProfile.objects.select_related("user").all(),
        empty_label="— Select a doctor —",
        label="Doctor",
    )
    scheduled_at = forms.DateTimeField(
        label="Scheduled Date & Time",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"],
    )
    notes = forms.CharField(widget=forms.Textarea(attrs={"rows": 4}), required=False, label="Notes")


    def save(self, *, patient: PatientProfile, created_by) -> Appointment:
        doctor: DoctorProfile = self.cleaned_data["doctor"]
        scheduled_at = self.cleaned_data["scheduled_at"]
        notes = self.cleaned_data.get("notes", "")

        return Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            created_by=created_by,
            scheduled_at=scheduled_at,
            notes=notes,
        )

