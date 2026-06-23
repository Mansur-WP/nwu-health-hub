from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from accounts.auth import role_required
from accounts.models import User
from appointments.models import Appointment
from doctors.models import DoctorProfile
from patients.models import PatientProfile
from payments.models import Payment
from pharmacists.models import PharmacistProfile
from prescriptions.models import Prescription

from .forms import DoctorCreateForm, StaffCreateForm


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return dashboard_stats(request)


@login_required
@role_required("admin")
def add_staff(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = StaffCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard-home")
    else:
        form = StaffCreateForm()

    return render(request, "dashboard/staff_form.html", {"form": form})


@login_required
@role_required("admin")
def add_doctor(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DoctorCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard-home")
    else:
        form = DoctorCreateForm()

    return render(request, "dashboard/doctor_form.html", {"form": form})


@login_required
@role_required("admin")
def delete_staff(request: HttpRequest, user_id: int) -> HttpResponse:
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        from django.contrib import messages
        messages.success(request, f"Staff member '{user.full_name or user.email}' has been deleted.")
        user.delete()
        return redirect("dashboard:staff-list")
    return render(request, "dashboard/staff_delete_confirm.html", {"staff_user": user})


@login_required
@role_required("admin")
def approve_staff(request: HttpRequest, user_id: int) -> HttpResponse:
    """Toggle a pharmacist's approval status between APPROVED / REJECTED / PENDING."""
    from django.contrib import messages

    profile = get_object_or_404(PharmacistProfile, user_id=user_id)
    if request.method == "POST":
        action = request.POST.get("action", "approve")
        name = profile.user.full_name or profile.user.email
        if action == "approve":
            profile.approval_status = PharmacistProfile.ApprovalStatus.APPROVED
            messages.success(request, f"{name} has been approved.")
        elif action == "reject":
            profile.approval_status = PharmacistProfile.ApprovalStatus.REJECTED
            messages.warning(request, f"{name} has been rejected.")
        elif action == "pending":
            profile.approval_status = PharmacistProfile.ApprovalStatus.PENDING
            messages.info(request, f"{name} reset to pending.")
        profile.save(update_fields=["approval_status"])
    return redirect("dashboard:staff-list")


@login_required
@role_required("admin")
def delete_doctor(
    request: HttpRequest,
    doctor_user_id: int,
) -> HttpResponse:
    doctor = get_object_or_404(DoctorProfile, user_id=doctor_user_id)
    if request.method == "POST":
        from django.contrib import messages
        messages.success(request, f"Dr. {doctor.user.full_name or doctor.user.email} has been deleted.")
        doctor.user.delete()
        return redirect("dashboard:doctor-list")
    return render(request, "dashboard/doctor_delete_confirm.html", {"doctor": doctor})


@login_required
@role_required("admin")
def approve_doctor(request: HttpRequest, doctor_user_id: int) -> HttpResponse:
    """Toggle a doctor's approval status between APPROVED and PENDING."""
    from django.contrib import messages

    doctor = get_object_or_404(DoctorProfile, user_id=doctor_user_id)
    if request.method == "POST":
        action = request.POST.get("action", "approve")
        if action == "approve":
            doctor.approval_status = DoctorProfile.ApprovalStatus.APPROVED
            messages.success(
                request,
                f"Dr. {doctor.user.full_name or doctor.user.email} has been approved.",
            )
        elif action == "reject":
            doctor.approval_status = DoctorProfile.ApprovalStatus.REJECTED
            messages.warning(
                request,
                f"Dr. {doctor.user.full_name or doctor.user.email} has been rejected.",
            )
        elif action == "pending":
            doctor.approval_status = DoctorProfile.ApprovalStatus.PENDING
            messages.info(
                request,
                f"Dr. {doctor.user.full_name or doctor.user.email} reset to pending.",
            )
        doctor.save(update_fields=["approval_status"])
    return redirect("dashboard:doctor-list")


@login_required
@role_required("admin")
def verify_payments(request: HttpRequest) -> HttpResponse:
    from django.contrib import messages
    pending_count = Payment.objects.filter(status=Payment.Status.PENDING).count()
    if request.method == "POST":
        Payment.objects.filter(status=Payment.Status.PENDING).update(
            status=Payment.Status.PAID,
            paid_at=timezone.now(),
        )
        messages.success(request, f"Successfully verified {pending_count} pending payments.")
        return redirect("dashboard:dashboard-home")

    return render(
        request,
        "dashboard/payments_verify_confirm.html",
        {"pending_count": pending_count},
    )


@login_required
@role_required("admin")
def dashboard_stats(request: HttpRequest) -> HttpResponse:
    total_patients = PatientProfile.objects.count()
    total_doctors = DoctorProfile.objects.count()
    total_appointments = Appointment.objects.count()
    total_payments = Payment.objects.count()
    total_prescriptions = Prescription.objects.count()

    appt_status_counts = (
        Appointment.objects.values("status").annotate(c=Count("id"))
    )
    chart_labels = [x["status"] for x in appt_status_counts]
    chart_values = [x["c"] for x in appt_status_counts]

    payment_pending_count = Payment.objects.filter(
        status=Payment.Status.PENDING
    ).count()

    recent_prescriptions = Prescription.objects.select_related(
        "patient", "doctor"
    ).order_by("-date")[:8]

    return render(
        request,
        "dashboard/index.html",
        {
            "stats": {
                "total_patients": total_patients,
                "total_doctors": total_doctors,
                "total_appointments": total_appointments,
                "total_payments": total_payments,
                "total_prescriptions": total_prescriptions,
            },
            "chart": {
                "labels": chart_labels,
                "values": chart_values,
            },
            "payment_pending_count": payment_pending_count,
            "prescriptions": recent_prescriptions,
        },
    )


@login_required
@role_required("admin")
def list_staff(request: HttpRequest) -> HttpResponse:
    """List all pharmacist profiles with their approval status."""
    staff_profiles = PharmacistProfile.objects.select_related("user").order_by(
        "-user__date_joined"
    )
    return render(request, "dashboard/staff_list.html", {"staff_profiles": staff_profiles})


@login_required
@role_required("admin")
def list_doctors(request: HttpRequest) -> HttpResponse:
    """List all doctor profiles."""
    doctors = DoctorProfile.objects.select_related("user").order_by(
        "user__last_name", "user__first_name"
    )
    return render(request, "dashboard/doctor_list.html", {"doctors": doctors})


@login_required
@role_required("admin")
def list_patients(request: HttpRequest) -> HttpResponse:
    """List all patient profiles."""
    patients = PatientProfile.objects.select_related("user").order_by(
        "user__last_name", "user__first_name"
    )
    return render(request, "dashboard/patient_list.html", {"patients": patients})


@login_required
@role_required("admin")
def delete_patient(request: HttpRequest, patient_user_id: int) -> HttpResponse:
    """Delete a patient user account."""
    user = get_object_or_404(User, id=patient_user_id)
    if request.method == "POST":
        from django.contrib import messages
        messages.success(request, f"Patient {user.full_name or user.email} deleted successfully.")
        user.delete()
        return redirect("dashboard:patient-list")
    return render(request, "dashboard/patient_delete_confirm.html", {"target_user": user})
