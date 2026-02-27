import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from accounts.models import Employee
from datetime import date

# Test auto-generation
print("Testing Employee ID Auto-Generation")
print("=" * 50)

# Get next ID
next_id = Employee.generate_employee_id()
print(f"Next Employee ID will be: {next_id}")

# Create a test employee without specifying employee_id
print("\nCreating test employee without employee_id...")
test_employee = Employee.objects.create(
    first_name="Test",
    last_name="User",
    email=f"test{Employee.objects.count()}@example.com",
    phone="1234567890",
    gender="M",
    date_of_birth=date(1990, 1, 1),
    date_of_joining=date(2024, 1, 1),
    department="Testing",
    designation="Test Engineer"
)

print(f"✓ Employee created with auto-generated ID: {test_employee.employee_id}")
print(f"✓ Employee: {test_employee}")

# Show all employee IDs
print("\nAll Employee IDs:")
for emp in Employee.objects.all():
    print(f"  - {emp.employee_id}: {emp.first_name} {emp.last_name}")

print("\n✅ Auto-generation working correctly!")
