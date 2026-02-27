import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.contrib.auth.models import User

print("Resetting admin password...")
print("=" * 50)

try:
    admin = User.objects.get(username='admin')
    admin.set_password('admin123')
    admin.save()
    print("✓ Password reset successfully!")
    print(f"Username: admin")
    print(f"Password: admin123")
    print()
    print("You can now login with these credentials.")
except User.DoesNotExist:
    print("Admin user not found. Creating...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✓ Admin user created!")
    print(f"Username: admin")
    print(f"Password: admin123")
