from __future__ import annotations

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.auth import role_required
from appointments.models import Appointment
from patients.forms import BookAppointmentForm, PatientProfileForm
from patients.models import PatientProfile
from payments.models import Payment


def _get_patient_profile_or_404(user) -> PatientProfile:
    return get_object_or_404(PatientProfile, user=user)


@role_required("patient")
def patient_profile_view(request: HttpRequest) -> HttpResponse:
    patient = _get_patient_profile_or_404(request.user)
    return render(
        request,
        "patients/patient_profile.html",
        {"patient": patient},
    )


@role_required("patient")
def patient_profile_update_view(request: HttpRequest) -> HttpResponse:
    patient = _get_patient_profile_or_404(request.user)

    if request.method == "POST":
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect(reverse("patients:patient-profile"))
    else:
        form = PatientProfileForm(instance=patient)

    return render(
        request,
        "patients/patient_profile_edit.html",
        {"form": form, "patient": patient},
    )


@role_required("patient")
def patient_appointments_list_view(request: HttpRequest) -> HttpResponse:
    patient = _get_patient_profile_or_404(request.user)

    appointments = (
        Appointment.objects.filter(patient=patient)
        .select_related("doctor__user")
        .prefetch_related("payment_set")
        .order_by("-scheduled_at")
    )

    # Annotate each appointment with its payment object for template access
    for appt in appointments:
        payments = list(appt.payment_set.all())
        if payments:
            appt.payment_obj = payments[0]
            appt.is_paid = payments[0].status == Payment.Status.PAID
        else:
            appt.payment_obj = None
            appt.is_paid = False

    return render(
        request,
        "patients/patient_appointments.html",
        {"appointments": appointments},
    )


@role_required("patient")
def patient_book_appointment_view(request: HttpRequest) -> HttpResponse:
    patient = _get_patient_profile_or_404(request.user)

    if request.method == "POST":
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(patient=patient, created_by=request.user)
            from decimal import Decimal
            Payment.objects.create(
                appointment=appointment,
                patient=patient,
                amount=Decimal("150.00"),
                status=Payment.Status.PENDING,
                created_by=request.user
            )
            messages.success(
                request,
                f"Appointment booked for {appointment.scheduled_at}. A payment invoice has been generated.",
            )
            return redirect(reverse("patients:patient-appointments"))
    else:
        form = BookAppointmentForm()

    return render(
        request,
        "patients/patient_book_appointment.html",
        {"form": form},
    )


@role_required("patient")
def patient_cancel_appointment_confirm_view(
    request: HttpRequest, appointment_id: int
) -> HttpResponse:
    patient = _get_patient_profile_or_404(request.user)
    appointment = get_object_or_404(
        Appointment, id=appointment_id, patient=patient
    )

    if appointment.status == Appointment.Status.CANCELLED:
        messages.info(request, "Appointment is already cancelled.")
        return redirect(reverse("patients:patient-appointments"))

    if request.method == "POST":
        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=["status"])
        messages.success(request, "Appointment cancelled.")
        return redirect(reverse("patients:patient-appointments"))

    return render(
        request,
        "patients/patient_cancel_appointment_confirm.html",
        {"appointment": appointment},
    )


@role_required("patient")
def patient_payment_history_view(request: HttpRequest) -> HttpResponse:
    patient = _get_patient_profile_or_404(request.user)

    payments = (
        Payment.objects.filter(patient=patient)
        .select_related("appointment__doctor__user", "appointment")
        .order_by("-paid_at")
    )

    return render(
        request,
        "patients/patient_payment_history.html",
        {"payments": payments},
    )

