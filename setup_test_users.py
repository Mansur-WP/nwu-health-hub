import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms.settings')
django.setup()

from accounts.models import User
from pharmacists.models import PharmacistProfile

# Create admin
if not User.objects.filter(email='admin@test.com').exists():
    User.objects.create_superuser('admin@test.com', 'password123')
    print("Created admin@test.com / password123")

# Create pharmacist
if not User.objects.filter(email='pharm@test.com').exists():
    user = User.objects.create_user('pharm@test.com', 'password123', role=User.Role.PHARMACIST)
    PharmacistProfile.objects.create(user=user, phone="123456789")
    print("Created pharm@test.com / password123")

print("Users setup complete.")
