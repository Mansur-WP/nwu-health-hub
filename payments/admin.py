from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("appointment", "patient", "amount", "status", "paid_at")
    list_filter = ("status",)
    search_fields = ("patient__user__email",)
    ordering = ("-paid_at",)
