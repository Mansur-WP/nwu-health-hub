from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from accounts.auth import role_required
from .models import Payment

@login_required
@role_required("admin", "doctor", "patient", "pharmacist")
def payment_list(request):
    if request.user.role == "patient":
        payments = Payment.objects.filter(patient__user=request.user).order_by("-id")
    else:
        payments = Payment.objects.all().order_by("-id")
    return render(request, "payments/payment_list.html", {"payments": payments})

@login_required
@role_required("patient")
def payment_checkout(request, pk: int):
    payment = get_object_or_404(Payment, pk=pk, patient__user=request.user)
    
    if payment.status == Payment.Status.PAID:
        return redirect("payments:payment-receipt", pk=payment.pk)
        
    if request.method == "POST":
        payment.status = Payment.Status.PAID
        payment.paid_at = timezone.now()
        payment.save(update_fields=["status", "paid_at"])
        messages.success(request, "Payment successful! Receipt generated.")
        return redirect("payments:payment-receipt", pk=payment.pk)
        
    return render(request, "payments/checkout.html", {"payment": payment})

@login_required
@role_required("admin", "patient")
def payment_receipt(request, pk: int):
    if request.user.role == "patient":
        payment = get_object_or_404(Payment, pk=pk, patient__user=request.user, status=Payment.Status.PAID)
    else:
        payment = get_object_or_404(Payment, pk=pk, status=Payment.Status.PAID)
        
    return render(request, "payments/receipt.html", {"payment": payment})

@login_required
@role_required("admin")
def payment_refund(request, pk: int):
    payment = get_object_or_404(Payment, pk=pk, status=Payment.Status.PAID)
    
    if request.method == "POST":
        payment.status = Payment.Status.REFUNDED
        payment.save(update_fields=["status"])
        messages.success(request, f"Payment #{payment.pk} refunded successfully.")
        return redirect("payments:payment-list")
        
    return render(request, "payments/refund_confirm.html", {"payment": payment})

