from django import forms
from django.contrib.auth.hashers import make_password

from accounts.models import User
from doctors.models import DoctorProfile


class StaffCreateForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(
        choices=[("pharmacist", "Pharmacist"), ("patient", "Patient")]
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def save(self) -> User:
        role = self.cleaned_data["role"]
        user = User.objects.create(
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data.get("first_name", ""),
            last_name=self.cleaned_data.get("last_name", ""),
            role=role,
            is_active=True,
            is_staff=False,
            password=make_password(self.cleaned_data["password"]),
        )
        # For profile-based roles, create the corresponding profile.
        if role == "doctor":
            DoctorProfile.objects.create(user=user)
        elif role == "pharmacist":
            from pharmacists.models import PharmacistProfile

            PharmacistProfile.objects.create(user=user)
        elif role == "patient":
            from patients.models import PatientProfile

            PatientProfile.objects.create(user=user)

        return user


class DoctorCreateForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    specialization = forms.CharField(required=False)
    phone = forms.CharField(required=False)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email

    def save(self) -> User:
        user = User.objects.create(
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data.get("first_name", ""),
            last_name=self.cleaned_data.get("last_name", ""),
            role="doctor",
            is_active=True,
            is_staff=False,
            password=make_password(self.cleaned_data["password"]),
        )
        DoctorProfile.objects.create(
            user=user,
            specialization=self.cleaned_data.get("specialization", ""),
            phone=self.cleaned_data.get("phone", ""),
        )
        return user

