from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.auth import role_required
from doctors.models import DoctorProfile
from patients.models import PatientProfile

from .forms import PrescriptionCreateForm
from .models import Prescription


@login_required
@role_required("doctor")
def prescription_create(request):
    if request.method == "POST":
        form = PrescriptionCreateForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = get_object_or_404(
                DoctorProfile, user=request.user
            )
            # MVP: associate to a patient profile. In a fuller flow this
            # would come from the Appointment/patient selection.
            prescription.patient = get_object_or_404(
                PatientProfile, user__role="patient"
            )
            prescription.save()
            return redirect("prescriptions:prescription-list")

    else:
        form = PrescriptionCreateForm()

    return render(
        request,
        "prescriptions/prescription_create.html",
        {"form": form},
    )


@login_required
@role_required("admin", "doctor", "pharmacist", "patient")
def prescription_list(request):
    qs = Prescription.objects.select_related("doctor", "patient")

    if request.user.role == "doctor":
        doctor = get_object_or_404(DoctorProfile, user=request.user)
        qs = qs.filter(doctor=doctor)
    elif request.user.role == "patient":
        patient = get_object_or_404(PatientProfile, user=request.user)
        qs = qs.filter(patient=patient)

    if request.user.role == "patient":
        return render(
            request,
            "patients/patient_prescription_list.html",
            {"prescriptions": qs.order_by("-date")},
        )
    else:
        return render(
            request,
            "prescriptions/prescription_list.html",
            {"prescriptions": qs.order_by("-date")},
        )



from django.db import transaction
from django.contrib import messages
from .forms import PrescriptionCreateForm, DispensePrescriptionForm
from pharmacists.models import MedicationInventory

@login_required
@role_required("pharmacist")
def dispense_prescription(request, pk: int):
    prescription = get_object_or_404(Prescription, pk=pk)

    if prescription.status != Prescription.Status.PENDING:
        return redirect("prescriptions:prescription-list")

    if request.method == "POST":
        form = DispensePrescriptionForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data["inventory_item"]
            quantity = form.cleaned_data["quantity"]

            try:
                with transaction.atomic():
                    # Lock the row for update
                    locked_item = MedicationInventory.objects.select_for_update().get(pk=item.pk)
                    
                    if locked_item.stock_quantity >= quantity:
                        locked_item.stock_quantity -= quantity
                        locked_item.save()
                        
                        prescription.status = Prescription.Status.DISPENSED
                        prescription.save(update_fields=["status"])
                        
                        messages.success(request, f"Dispensed {quantity}x {locked_item.name}. Stock is now {locked_item.stock_quantity}.")
                        return redirect("prescriptions:prescription-list")
                    else:
                        messages.error(request, f"Insufficient stock! Available: {locked_item.stock_quantity}.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = DispensePrescriptionForm()

    return render(
        request,
        "prescriptions/prescription_dispense_confirm.html",
        {"prescription": prescription, "form": form},
    )

