from __future__ import annotations

from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False, max_length=150)
    last_name = forms.CharField(required=False, max_length=150)

    role = forms.ChoiceField(required=True)

    password1 = forms.CharField(
        required=True, widget=forms.PasswordInput, label="Password"
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput,
        label="Confirm password",
    )

    def __init__(self, *args, **kwargs):
        from .models import User

        super().__init__(*args, **kwargs)
        self.fields["role"].choices = User.Role.choices

    def clean_email(self):
        from .models import User

        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned


