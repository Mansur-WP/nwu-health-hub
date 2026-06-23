from django.urls import path

from . import views

app_name = "doctors"

urlpatterns = [
    path(
        "appointments/",
        views.doctor_appointments_list_view,
        name="doctor-appointments",
    ),
    path(
        "appointments/<int:appointment_id>/approve/",
        views.doctor_appointment_approve_confirm_view,
        name="doctor-appointment-approve",
    ),
    path(
        "appointments/<int:appointment_id>/cancel/",
        views.doctor_appointment_cancel_confirm_view,
        name="doctor-appointment-cancel",
    ),
    path(
        "patients/<int:patient_id>/history/",
        views.doctor_patient_history_view,
        name="doctor-patient-history",
    ),
    path(
        "appointments/<int:appointment_id>/prescriptions/new/",
        views.doctor_prescription_create_view,
        name="doctor-prescription-create",
    ),
    path(
        "prescriptions/<int:pk>/send/",
        views.doctor_send_prescription_view,
        name="doctor-prescription-send",
    ),
]


