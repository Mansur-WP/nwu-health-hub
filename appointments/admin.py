from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "scheduled_at", "status")
    list_filter = ("status", "scheduled_at")
    search_fields = ("patient__user__email", "doctor__user__email")
    ordering = ("-scheduled_at",)
