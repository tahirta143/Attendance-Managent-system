import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

print("Checking users in database...")
print("=" * 50)

users = User.objects.all()
print(f"Total users: {users.count()}")
print()

for user in users:
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is Active: {user.is_active}")
    print(f"Is Superuser: {user.is_superuser}")
    print("-" * 50)

print()
print("Testing authentication...")
user = authenticate(username='admin', password='admin123')
if user:
    print(f"✓ Authentication successful for: {user.username}")
else:
    print("✗ Authentication failed")
    print()
    print("Creating superuser 'admin' with password 'admin123'...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✓ Superuser created!")
