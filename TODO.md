# TODO - Doctor/Pharmacy approval gating

## Step 1 (setup)
- [ ] Add approval status fields to `DoctorProfile` and `PharmacistProfile` (default: pending)

## Step 2 (gate)
- [ ] Implement `doctor_approved_required` / `pharmacist_approved_required` decorator in `accounts/auth.py`
- [ ] Add waiting page view in `accounts/views.py` + route in `accounts/urls.py`
- [ ] Add `templates/accounts/waiting_approval.html`

## Step 3 (restrict access)
- [ ] Apply approval gate to all relevant doctor views in `doctors/views.py`
- [ ] Apply approval gate to all relevant pharmacist views in `pharmacists/views.py`

## Step 4 (redirect after login/register)
- [ ] Update `_role_redirect_name()` and register/login redirects so pending users land on waiting page

## Step 5 (admin approval)
- [ ] Update `doctors/admin.py` and `pharmacists/admin.py` to allow setting approval_status (and display it)

## Step 6 (migrations + verify)
- [ ] Create migrations and apply (`makemigrations`, `migrate`)
- [ ] Manual test: register doctor/pharmacist -> waiting page; admin approves -> dashboard works

