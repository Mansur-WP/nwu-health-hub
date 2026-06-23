from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("medicine", "patient", "doctor", "date", "status")
    list_filter = ("status", "date")
    search_fields = ("medicine", "patient__user__email", "doctor__user__email")
    ordering = ("-date",)
