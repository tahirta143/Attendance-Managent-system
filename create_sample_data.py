import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Role, Permission, UserRole, Employee, Attendance
from datetime import date, time

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✓ Superuser created: admin / admin123')

# Create roles
admin_role, _ = Role.objects.get_or_create(
    name='Administrator',
    defaults={'description': 'Full system access'}
)
manager_role, _ = Role.objects.get_or_create(
    name='Manager',
    defaults={'description': 'Can manage employees and attendance'}
)
employee_role, _ = Role.objects.get_or_create(
    name='Employee',
    defaults={'description': 'Basic employee access'}
)
print('✓ Roles created')

# Create permissions
permissions_data = [
    ('View Dashboard', 'view_dashboard', 'Can view dashboard'),
    ('Manage Users', 'manage_users', 'Can create, edit, delete users'),
    ('Manage Employees', 'manage_employees', 'Can manage employee records'),
    ('Mark Attendance', 'mark_attendance', 'Can mark attendance'),
    ('View Reports', 'view_reports', 'Can view attendance reports'),
]

for name, codename, desc in permissions_data:
    Permission.objects.get_or_create(
        codename=codename,
        defaults={'name': name, 'description': desc}
    )
print('✓ Permissions created')

# Create sample employees
employees_data = [
    {
        'employee_id': 'EMP001',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@company.com',
        'phone': '1234567890',
        'gender': 'M',
        'date_of_birth': date(1990, 5, 15),
        'date_of_joining': date(2020, 1, 10),
        'department': 'IT',
        'designation': 'Software Engineer'
    },
    {
        'employee_id': 'EMP002',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@company.com',
        'phone': '0987654321',
        'gender': 'F',
        'date_of_birth': date(1992, 8, 20),
        'date_of_joining': date(2021, 3, 15),
        'department': 'HR',
        'designation': 'HR Manager'
    },
    {
        'employee_id': 'EMP003',
        'first_name': 'Mike',
        'last_name': 'Johnson',
        'email': 'mike.johnson@company.com',
        'phone': '5551234567',
        'gender': 'M',
        'date_of_birth': date(1988, 12, 5),
        'date_of_joining': date(2019, 6, 1),
        'department': 'Finance',
        'designation': 'Accountant'
    },
    {
        'employee_id': 'EMP004',
        'first_name': 'Sarah',
        'last_name': 'Williams',
        'email': 'sarah.williams@company.com',
        'phone': '5559876543',
        'gender': 'F',
        'date_of_birth': date(1995, 3, 25),
        'date_of_joining': date(2022, 1, 20),
        'department': 'IT',
        'designation': 'UI/UX Designer'
    },
    {
        'employee_id': 'EMP005',
        'first_name': 'David',
        'last_name': 'Brown',
        'email': 'david.brown@company.com',
        'phone': '5552223333',
        'gender': 'M',
        'date_of_birth': date(1991, 7, 10),
        'date_of_joining': date(2020, 9, 5),
        'department': 'Marketing',
        'designation': 'Marketing Manager'
    }
]

for emp_data in employees_data:
    Employee.objects.get_or_create(
        employee_id=emp_data['employee_id'],
        defaults=emp_data
    )
print('✓ Sample employees created')

# Create sample attendance for the past 7 days
from datetime import timedelta
import random

today = date.today()
employees = Employee.objects.all()

# Attendance patterns for variety
attendance_patterns = [
    {'status': 'present', 'check_in': time(9, 0), 'check_out': time(17, 30)},
    {'status': 'present', 'check_in': time(8, 45), 'check_out': time(17, 15)},
    {'status': 'late', 'check_in': time(10, 15), 'check_out': time(18, 0)},
    {'status': 'present', 'check_in': time(9, 10), 'check_out': time(17, 45)},
    {'status': 'leave', 'check_in': None, 'check_out': None},
    {'status': 'absent', 'check_in': None, 'check_out': None},
]

# Create attendance for last 7 days
for day_offset in range(7):
    attendance_date = today - timedelta(days=day_offset)
    
    for employee in employees:
        # Randomly select attendance pattern (mostly present)
        if random.random() < 0.8:  # 80% present
            pattern = attendance_patterns[random.randint(0, 3)]
        else:  # 20% leave/absent
            pattern = attendance_patterns[random.randint(4, 5)]
        
        Attendance.objects.get_or_create(
            employee=employee,
            date=attendance_date,
            defaults=pattern
        )

print('✓ Sample attendance created for the past 7 days')

print('\n✅ Sample data created successfully!')
print('\nLogin credentials:')
print('Username: admin')
print('Password: admin123')
