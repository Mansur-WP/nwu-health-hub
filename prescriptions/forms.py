from django import forms

from .models import Prescription
from pharmacists.models import MedicationInventory


class PrescriptionCreateForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            "medicine",
            "dosage",
            "instructions",
            "date",
        ]
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "medicine": forms.TextInput(attrs={"class": "form-control"}),
            "dosage": forms.TextInput(attrs={"class": "form-control"}),
            "instructions": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }

class DispensePrescriptionForm(forms.Form):
    inventory_item = forms.ModelChoiceField(
        queryset=MedicationInventory.objects.order_by("name"),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Select Inventory Item to Deduct"
    )
    quantity = forms.IntegerField(
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="Quantity to Deduct"
    )
