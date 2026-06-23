from django.contrib import admin
from .models import PharmacistProfile, MedicationInventory

@admin.register(PharmacistProfile)
class PharmacistProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")
    search_fields = ("user__email", "phone")

@admin.register(MedicationInventory)
class MedicationInventoryAdmin(admin.ModelAdmin):
    list_display = ("name", "stock_quantity", "last_updated")
    search_fields = ("name",)
    list_filter = ("last_updated",)
