from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="dashboard-home"),
    path("staff/add/", views.add_staff, name="staff-add"),
    path(
        "staff/delete/<int:user_id>/",
        views.delete_staff,
        name="staff-delete",
    ),
    path(
        "staff/approve/<int:user_id>/",
        views.approve_staff,
        name="staff-approve",
    ),
    path("doctors/add/", views.add_doctor, name="doctor-add"),
    path(
        "doctors/delete/<int:doctor_user_id>/",
        views.delete_doctor,
        name="doctor-delete",
    ),
    path(
        "doctors/approve/<int:doctor_user_id>/",
        views.approve_doctor,
        name="doctor-approve",
    ),
    path(
        "payments/verify/",
        views.verify_payments,
        name="payments-verify",
    ),
    path("stats/", views.dashboard_stats, name="dashboard-stats"),
    path("staff/", views.list_staff, name="staff-list"),
    path("doctors/", views.list_doctors, name="doctor-list"),
    path("patients/", views.list_patients, name="patient-list"),
    path(
        "patients/delete/<int:patient_user_id>/",
        views.delete_patient,
        name="patient-delete",
    ),
]


