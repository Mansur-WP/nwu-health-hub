"""
URL configuration for hms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from home import views as home_views


urlpatterns = [
    # path("admin/", admin.site.urls),

    # Homepage
    path("", home_views.home_view, name="home"),
    path("services/", home_views.services_view, name="services"),
    path("our-doctors/", home_views.doctors_page_view, name="doctors-page"),
    path("contact/", home_views.contact_view, name="contact"),

    # Authentication + registration
    path("", include("accounts.urls")),




    # Dashboard and role landing pages
    path("dashboard/", include("dashboard.urls")),
    path("patients/", include("patients.urls")),
    path("doctors/", include("doctors.urls")),
    path("pharmacists/", include("pharmacists.urls")),
    path("appointments/", include("appointments.urls")),
    path("payments/", include("payments.urls")),
    path("prescriptions/", include("prescriptions.urls")),
]

