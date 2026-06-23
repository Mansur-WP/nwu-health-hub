from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.auth import role_required


@login_required
@role_required("admin", "doctor", "patient")
def appointment_list(request):
    return render(request, "appointments/appointment_list.html")

