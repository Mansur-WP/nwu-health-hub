from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.auth import role_approved_required, role_required

from .forms import InventoryForm
from .models import MedicationInventory


@login_required
@role_approved_required("pharmacist")
@role_required("pharmacist")
def list_pharmacists(request):
    return render(request, "pharmacists/pharmacist_list.html")


@login_required
@role_approved_required("pharmacist")
@role_required("pharmacist", "admin")
def inventory_list(request):
    inventory = MedicationInventory.objects.order_by("name")
    return render(
        request,
        "pharmacists/inventory_list.html",
        {"inventory": inventory},
    )


@login_required
@role_approved_required("pharmacist")
@role_required("pharmacist", "admin")
def inventory_create(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory item created successfully.")
            return redirect("pharmacists:inventory-list")
    else:
        form = InventoryForm()

    return render(
        request,
        "pharmacists/inventory_form.html",
        {"form": form},
    )


@login_required
@role_approved_required("pharmacist")
@role_required("pharmacist", "admin")
def inventory_update(request, pk: int):
    item = get_object_or_404(MedicationInventory, pk=pk)
    if request.method == "POST":
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory item updated successfully.")
            return redirect("pharmacists:inventory-list")
    else:
        form = InventoryForm(instance=item)

    return render(
        request,
        "pharmacists/inventory_form.html",
        {"form": form, "item": item},
    )

