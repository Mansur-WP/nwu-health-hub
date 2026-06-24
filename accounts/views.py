from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .auth import role_required

from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_admin(request):
    User = get_user_model()

    email = "admin@nwu.com"

    if User.objects.filter(email=email).exists():
        return HttpResponse("Admin already exists.")

    User.objects.create_superuser(
        email=email,
        password="Admin12345"
    )

    return HttpResponse("Admin created successfully.")

def _role_redirect_name(role: str) -> str:
    """Map user roles to their landing URL names."""

    mapping = {
        "admin": "dashboard:dashboard-home",
        "patient": "patients:patient-profile",
        "doctor": "doctors:doctor-appointments",
        "pharmacist": "pharmacists:pharmacist-list",
    }
    return mapping.get(role, "dashboard:dashboard-home")


def _is_profile_approved(user) -> bool:
    """Return True if the user's role-profile is approved (or doesn't require approval)."""
    from accounts.models import User

    if user.role == User.Role.DOCTOR:
        from doctors.models import DoctorProfile
        try:
            return DoctorProfile.objects.get(user=user).approval_status == DoctorProfile.ApprovalStatus.APPROVED
        except Exception:
            return False
    if user.role == User.Role.PHARMACIST:
        from pharmacists.models import PharmacistProfile
        try:
            return PharmacistProfile.objects.get(user=user).approval_status == PharmacistProfile.ApprovalStatus.APPROVED
        except Exception:
            return False
    return True  # admin / patient don't need approval


def pending_approval_view(request: HttpRequest) -> HttpResponse:
    """Shown to doctors/pharmacists who are logged in but not yet approved."""
    return render(request, "accounts/waiting_approval.html")


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        # Unapproved doctors/pharmacists must NOT be sent to their dashboard
        # (which is protected) — that would cause an infinite redirect loop.
        if not _is_profile_approved(request.user):
            return redirect("accounts:pending-approval")
        return redirect(_role_redirect_name(request.user.role))

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if not _is_profile_approved(user):
                return redirect("accounts:pending-approval")
            return redirect(_role_redirect_name(user.role))
        messages.error(request, "Invalid credentials.")

    return render(request, "accounts/login.html")


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("accounts:login")


def register_view(request: HttpRequest) -> HttpResponse:
    from .forms import RegisterForm
    from .models import User

    if request.user.is_authenticated:
        return redirect(_role_redirect_name(request.user.role))

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                first_name=form.cleaned_data.get("first_name", ""),
                last_name=form.cleaned_data.get("last_name", ""),
                role=form.cleaned_data["role"],
            )
            # Create corresponding profile
            if user.role == User.Role.PATIENT:
                from patients.models import PatientProfile
                PatientProfile.objects.get_or_create(user=user)
            elif user.role == User.Role.DOCTOR:
                from doctors.models import DoctorProfile
                DoctorProfile.objects.get_or_create(user=user)
            elif user.role == User.Role.PHARMACIST:
                from pharmacists.models import PharmacistProfile
                PharmacistProfile.objects.get_or_create(user=user)

            login(request, user)
            if not _is_profile_approved(user):
                return redirect("accounts:pending-approval")
            return redirect(_role_redirect_name(user.role))
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
@role_required("admin")
def admin_home(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/admin_home.html")


