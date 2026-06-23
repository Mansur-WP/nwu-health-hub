from django.urls import path

from . import views

app_name = "prescriptions"

urlpatterns = [
    path("", views.prescription_list, name="prescription-list"),
    path("create/", views.prescription_create, name="prescription-create"),
    path(
        "dispense/<int:pk>/",
        views.dispense_prescription,
        name="prescription-dispense",
    ),
]

