from __future__ import annotations

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from accounts.auth import role_approved_required, role_required

from appointments.models import Appointment
from doctors.forms import PrescriptionForm
from doctors.models import DoctorProfile
from patients.models import PatientProfile
from payments.models import Payment
from prescriptions.models import Prescription


@login_required
@role_approved_required("doctor")
def doctor_appointments_list_view(request: HttpRequest) -> HttpResponse:

    doctor = get_object_or_404(DoctorProfile, user=request.user)
    appointments = (
        Appointment.objects.filter(doctor=doctor)
        .select_related("patient__user", "doctor__user")
        .prefetch_related("payment_set")
        .order_by("-scheduled_at")
    )
    # Annotate each appointment with its payment status for template access
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
        "doctors/doctor_appointments.html",
        {"appointments": appointments},
    )


@login_required
@role_approved_required("doctor")
def doctor_appointment_approve_confirm_view(

    request: HttpRequest, appointment_id: int
) -> HttpResponse:
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

    if appointment.status == Appointment.Status.APPROVED:
        messages.info(request, "Appointment is already approved.")
        return redirect(reverse("doctors:doctor-appointments"))

    if request.method == "POST":
        appointment.status = Appointment.Status.APPROVED
        appointment.save(update_fields=["status"])
        messages.success(request, "Appointment approved.")
        
        send_mail(
            "Appointment Approved",
            f"Your appointment on {appointment.scheduled_at.strftime('%B %d, %Y')} has been approved by Dr. {doctor.user.last_name}.",
            "no-reply@hms.com",
            [appointment.patient.user.email],
            fail_silently=True,
        )
        
        return redirect(reverse("doctors:doctor-appointments"))

    return render(
        request,
        "doctors/doctor_appointment_approve_confirm.html",
        {"appointment": appointment},
    )


@login_required
@role_approved_required("doctor")
def doctor_appointment_cancel_confirm_view(

    request: HttpRequest, appointment_id: int
) -> HttpResponse:
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

    if appointment.status == Appointment.Status.CANCELLED:
        messages.info(request, "Appointment is already cancelled.")
        return redirect(reverse("doctors:doctor-appointments"))

    if request.method == "POST":
        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=["status"])
        messages.success(request, "Appointment cancelled.")
        
        send_mail(
            "Appointment Cancelled",
            f"Your appointment on {appointment.scheduled_at.strftime('%B %d, %Y')} has been cancelled by Dr. {doctor.user.last_name}.",
            "no-reply@hms.com",
            [appointment.patient.user.email],
            fail_silently=True,
        )
        
        return redirect(reverse("doctors:doctor-appointments"))

    return render(
        request,
        "doctors/doctor_appointment_cancel_confirm.html",
        {"appointment": appointment},
    )


@login_required
@role_approved_required("doctor")
def doctor_patient_history_view(

    request: HttpRequest, patient_id: int
) -> HttpResponse:
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    patient = get_object_or_404(PatientProfile, pk=patient_id)

    appointments = (
        Appointment.objects.filter(doctor=doctor, patient=patient)
        .select_related("patient__user", "doctor__user")
        .order_by("-scheduled_at")
    )

    prescriptions = Prescription.objects.filter(doctor=doctor, patient=patient).order_by("-date")

    return render(
        request,
        "doctors/doctor_patient_history.html",
        {
            "patient": patient,
            "appointments": appointments,
            "prescriptions": prescriptions,
        },
    )


@login_required
@role_approved_required("doctor")
def doctor_prescription_create_view(

    request: HttpRequest, appointment_id: int
) -> HttpResponse:
    doctor = get_object_or_404(DoctorProfile, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

    # --- Payment enforcement: block prescription if appointment is unpaid ---
    payment = Payment.objects.filter(appointment=appointment).first()
    is_paid = payment and payment.status == Payment.Status.PAID
    if not is_paid:
        messages.warning(
            request,
            "Cannot write prescription — the patient has not paid for this appointment yet.",
        )
        return redirect(reverse("doctors:doctor-appointments"))

    if hasattr(appointment, "prescription"):
        messages.info(request, "Prescription already exists for this appointment.")
        return redirect(reverse("doctors:doctor-appointments"))

    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save_with_appointment(
                appointment=appointment,
                created_by=request.user,
            )
            messages.success(request, "Prescription created.")
            return redirect(
                reverse(
                    "doctors:doctor-patient-history",
                    args=[appointment.patient_id],
                )
            )
    else:
        form = PrescriptionForm()
        prescription = None

    return render(
        request,
        "doctors/doctor_prescription_form.html",
        {"appointment": appointment, "form": form},
    )

@login_required
@role_approved_required("doctor")
def doctor_send_prescription_view(request: HttpRequest, pk: int) -> HttpResponse:

    doctor = get_object_or_404(DoctorProfile, user=request.user)
    prescription = get_object_or_404(Prescription, pk=pk, doctor=doctor, status=Prescription.Status.DRAFT)
    
    if request.method == "POST":
        prescription.status = Prescription.Status.PENDING
        prescription.save(update_fields=["status"])
        messages.success(request, "Prescription sent to pharmacy.")
        
        send_mail(
            "Prescription Ready",
            f"Your prescription for {prescription.medicine} has been sent to the pharmacy by Dr. {doctor.user.last_name}.",
            "no-reply@hms.com",
            [prescription.patient.user.email, "pharmacy@hms.com"],
            fail_silently=True,
        )
        
    return redirect(reverse("doctors:doctor-patient-history", args=[prescription.patient_id]))

