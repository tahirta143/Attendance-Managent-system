import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from accounts.models import Employee, Attendance
from datetime import date, timedelta

today = date.today()

print("=== DATABASE VERIFICATION ===\n")

# Check employees
total_employees = Employee.objects.filter(is_active=True).count()
print(f"Total Active Employees: {total_employees}")

# Check today's attendance
present_today = Attendance.objects.filter(date=today, status='present').count()
absent_today = Attendance.objects.filter(date=today, status='absent').count()
leave_today = Attendance.objects.filter(date=today, status='leave').count()
late_today = Attendance.objects.filter(date=today, status='late').count()

print(f"\nToday's Attendance ({today}):")
print(f"  Present: {present_today}")
print(f"  Absent: {absent_today}")
print(f"  Leave: {leave_today}")
print(f"  Late: {late_today}")
print(f"  Total: {present_today + absent_today + leave_today + late_today}")

# Check weekly data
print(f"\nWeekly Attendance (Last 7 days):")
for i in range(6, -1, -1):
    check_date = today - timedelta(days=i)
    count = Attendance.objects.filter(date=check_date).count()
    present = Attendance.objects.filter(date=check_date, status='present').count()
    print(f"  {check_date.strftime('%a %Y-%m-%d')}: {present} present / {count} total")

# Check departments
print(f"\nDepartment-wise Attendance (Today):")
departments = Employee.objects.values_list('department', flat=True).distinct()
for dept in departments:
    present_count = Attendance.objects.filter(
        date=today,
        status='present',
        employee__department=dept
    ).count()
    total_in_dept = Employee.objects.filter(department=dept, is_active=True).count()
    print(f"  {dept}: {present_count}/{total_in_dept} present")

print("\n✅ Verification complete!")
