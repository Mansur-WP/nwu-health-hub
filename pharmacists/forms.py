from django import forms
from .models import MedicationInventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = MedicationInventory
        fields = ["name", "stock_quantity", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "stock_quantity": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
