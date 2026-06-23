from __future__ import annotations

from typing import Iterable

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

# Dedicated URL for "not yet approved" — avoids redirecting back to login,
# which would immediately redirect back here (infinite loop).
_PENDING_APPROVAL_URL = "/accounts/pending-approval/"


def user_has_any_role(user, roles: Iterable[str]) -> bool:
    return getattr(user, "role", None) in set(roles)


def role_required(*roles: str):
    """Allow access only if request.user.role is in roles."""
    return user_passes_test(lambda u: user_has_any_role(u, roles))


def role_approved_required(role: str):
    """Allow access only if user's profile for that role is approved.

    On failure redirects to the pending-approval page (not the login page)
    so that authenticated-but-unapproved users don't get caught in an
    infinite login → appointments → login redirect loop.
    """

    def _is_approved(u) -> bool:
        if getattr(u, "role", None) != role:
            return False

        if role == "doctor":
            from doctors.models import DoctorProfile

            try:
                return (
                    DoctorProfile.objects.get(user=u).approval_status
                    == DoctorProfile.ApprovalStatus.APPROVED
                )
            except Exception:
                return False

        if role == "pharmacist":
            from pharmacists.models import PharmacistProfile

            try:
                return (
                    PharmacistProfile.objects.get(user=u).approval_status
                    == PharmacistProfile.ApprovalStatus.APPROVED
                )
            except Exception:
                return False

        return True

    # redirect_field_name=None keeps the URL clean (no ?next= appended)
    return user_passes_test(_is_approved, login_url=_PENDING_APPROVAL_URL, redirect_field_name=None)


class RoleRequiredMixin(UserPassesTestMixin):
    """CBV mixin: allow access only if user.role in required_roles."""

    required_roles: tuple[str, ...] = ()

    def test_func(self):
        return user_has_any_role(self.request.user, self.required_roles)

