from django.urls import path

from . import views

app_name = "patients"

urlpatterns = [
    path("profile/", views.patient_profile_view, name="patient-profile"),
    path(
        "profile/edit/",
        views.patient_profile_update_view,
        name="patient-profile-edit",
    ),
    path(
        "appointments/",
        views.patient_appointments_list_view,
        name="patient-appointments",
    ),
    path(
        "appointments/book/",
        views.patient_book_appointment_view,
        name="patient-book-appointment",
    ),
    path(
        "appointments/<int:appointment_id>/cancel/",
        views.patient_cancel_appointment_confirm_view,
        name="patient-appointment-cancel",
    ),
    path(
        "payments/",
        views.patient_payment_history_view,
        name="patient-payments",
    ),
]


