from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from appointments.models import Appointment
from prescriptions.models import Prescription
from doctors.models import DoctorProfile
from patients.models import PatientProfile


def home_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        from accounts.views import _role_redirect_name
        return redirect(_role_redirect_name(request.user.role))

    context = {
        "stat_appointments": Appointment.objects.count(),
        "stat_prescriptions": Prescription.objects.count(),
        "stat_doctors": DoctorProfile.objects.count(),
        "stat_patients": PatientProfile.objects.count(),
    }
    return render(request, "home.html", context)


def services_view(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/services.html")


def doctors_page_view(request: HttpRequest) -> HttpResponse:
    doctors = DoctorProfile.objects.select_related("user").all()
    return render(request, "pages/doctors.html", {"doctors": doctors})


def contact_view(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/contact.html")

