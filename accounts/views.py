from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, time
from .models import Role, Permission, RolePermission, UserRole, Employee, Attendance

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

@login_required
def dashboard(request):
    from datetime import timedelta
    from django.db.models import Count, Q
    
    today = timezone.now().date()
    total_employees = Employee.objects.filter(is_active=True).count()
    
    # Today's attendance
    present_today = Attendance.objects.filter(date=today, status='present').count()
    leave_today = Attendance.objects.filter(date=today, status='leave').count()
    late_today = Attendance.objects.filter(date=today, status='late').count()
    absent_today = Attendance.objects.filter(date=today, status='absent').count()
    
    # Weekly data (last 7 days)
    weekly_data = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        day_data = {
            'date': date,
            'present': Attendance.objects.filter(date=date, status='present').count(),
            'absent': Attendance.objects.filter(date=date, status='absent').count(),
            'leave': Attendance.objects.filter(date=date, status='leave').count(),
            'late': Attendance.objects.filter(date=date, status='late').count(),
        }
        weekly_data.append(day_data)
    
    # Department-wise attendance for today
    departments = Employee.objects.values('department').distinct()
    dept_attendance = []
    for dept in departments:
        dept_name = dept['department']
        present_count = Attendance.objects.filter(
            date=today,
            status='present',
            employee__department=dept_name
        ).count()
        dept_attendance.append({
            'department': dept_name,
            'present': present_count
        })
    
    context = {
        'total_employees': total_employees,
        'present_today': present_today,
        'leave_today': leave_today,
        'absent_today': absent_today,
        'late_today': late_today,
        'weekly_data': weekly_data,
        'dept_attendance': dept_attendance,
    }
    return render(request, 'dashboard.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def users_list(request):
    users = User.objects.all().select_related('user_role__role')
    return render(request, 'users/list.html', {'users': users})

@login_required
def user_create(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        user = User.objects.create_user(username=username, email=email, password=password,
                                       first_name=first_name, last_name=last_name)
        messages.success(request, 'User created successfully')
        return redirect('users_list')
    
    return render(request, 'users/create.html')

@login_required
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        messages.success(request, 'User updated successfully')
        return redirect('users_list')
    
    return render(request, 'users/edit.html', {'user': user})

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully')
    return redirect('users_list')

@login_required
def roles_list(request):
    roles = Role.objects.all()
    return render(request, 'roles/list.html', {'roles': roles})

@login_required
def role_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        Role.objects.create(name=name, description=description)
        messages.success(request, 'Role created successfully')
        return redirect('roles_list')
    
    return render(request, 'roles/create.html')

@login_required
def role_edit(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    
    if request.method == 'POST':
        role.name = request.POST['name']
        role.description = request.POST.get('description', '')
        role.save()
        messages.success(request, 'Role updated successfully')
        return redirect('roles_list')
    
    return render(request, 'roles/edit.html', {'role': role})

@login_required
def role_delete(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        role.delete()
        messages.success(request, 'Role deleted successfully')
    return redirect('roles_list')

@login_required
def permissions_list(request):
    permissions = Permission.objects.all()
    return render(request, 'permissions/list.html', {'permissions': permissions})

@login_required
def permission_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        codename = request.POST['codename']
        description = request.POST.get('description', '')
        Permission.objects.create(name=name, codename=codename, description=description)
        messages.success(request, 'Permission created successfully')
        return redirect('permissions_list')
    
    return render(request, 'permissions/create.html')

@login_required
def user_roles(request):
    user_roles = UserRole.objects.all().select_related('user', 'role')
    users = User.objects.all()
    roles = Role.objects.all()
    return render(request, 'user_roles/list.html', {
        'user_roles': user_roles,
        'users': users,
        'roles': roles
    })

@login_required
def assign_role(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        role_id = request.POST['role_id']
        user = get_object_or_404(User, id=user_id)
        role = get_object_or_404(Role, id=role_id)
        
        user_role, created = UserRole.objects.get_or_create(user=user)
        user_role.role = role
        user_role.save()
        messages.success(request, 'Role assigned successfully')
    
    return redirect('user_roles')

@login_required
def employees_list(request):
    search = request.GET.get('search', '')
    employees = Employee.objects.all()
    
    if search:
        employees = employees.filter(
            Q(employee_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    return render(request, 'employees/list.html', {'employees': employees, 'search': search})

@login_required
def employee_create(request):
    if request.method == 'POST':
        try:
            # Check if email already exists
            if Employee.objects.filter(email=request.POST['email']).exists():
                messages.error(request, 'An employee with this email already exists.')
                next_id = Employee.generate_employee_id()
                return render(request, 'employees/create.html', {
                    'next_employee_id': next_id,
                    'form_data': request.POST
                })
            
            employee = Employee.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                gender=request.POST['gender'],
                date_of_birth=request.POST['date_of_birth'],
                date_of_joining=request.POST['date_of_joining'],
                department=request.POST['department'],
                designation=request.POST['designation'],
            )
            messages.success(request, f'Employee created successfully with ID: {employee.employee_id}')
            return redirect('employees_list')
        except Exception as e:
            messages.error(request, f'Error creating employee: {str(e)}')
            next_id = Employee.generate_employee_id()
            return render(request, 'employees/create.html', {
                'next_employee_id': next_id,
                'form_data': request.POST
            })
    
    # Get next employee ID for display
    next_id = Employee.generate_employee_id()
    return render(request, 'employees/create.html', {'next_employee_id': next_id})

@login_required
def employee_edit(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        try:
            # Check if email is being changed and if new email already exists
            new_email = request.POST['email']
            if new_email != employee.email and Employee.objects.filter(email=new_email).exists():
                messages.error(request, 'An employee with this email already exists.')
                return render(request, 'employees/edit.html', {'employee': employee})
            
            employee.first_name = request.POST['first_name']
            employee.last_name = request.POST['last_name']
            employee.email = new_email
            employee.phone = request.POST['phone']
            employee.gender = request.POST['gender']
            employee.date_of_birth = request.POST['date_of_birth']
            employee.date_of_joining = request.POST['date_of_joining']
            employee.department = request.POST['department']
            employee.designation = request.POST['designation']
            employee.save()
            messages.success(request, 'Employee updated successfully')
            return redirect('employees_list')
        except Exception as e:
            messages.error(request, f'Error updating employee: {str(e)}')
            return render(request, 'employees/edit.html', {'employee': employee})
    
    return render(request, 'employees/edit.html', {'employee': employee})

@login_required
def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully')
    return redirect('employees_list')

@login_required
def attendance_list(request):
    date_filter = request.GET.get('date', timezone.now().date())
    search = request.GET.get('search', '')
    
    attendances = Attendance.objects.filter(date=date_filter).select_related('employee')
    
    if search:
        attendances = attendances.filter(
            Q(employee__employee_id__icontains=search) |
            Q(employee__first_name__icontains=search) |
            Q(employee__last_name__icontains=search)
        )
    
    return render(request, 'attendance/list.html', {
        'attendances': attendances,
        'date_filter': date_filter,
        'search': search
    })

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        date = request.POST['date']
        status = request.POST['status']
        check_in = request.POST.get('check_in', None)
        check_out = request.POST.get('check_out', None)
        remarks = request.POST.get('remarks', '')
        
        employee = get_object_or_404(Employee, id=employee_id)
        
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=date,
            defaults={
                'status': status,
                'check_in': check_in if check_in else None,
                'check_out': check_out if check_out else None,
                'remarks': remarks
            }
        )
        
        if not created:
            attendance.status = status
            attendance.check_in = check_in if check_in else None
            attendance.check_out = check_out if check_out else None
            attendance.remarks = remarks
            attendance.save()
        
        messages.success(request, 'Attendance marked successfully')
        return redirect('attendance_list')
    
    employees = Employee.objects.filter(is_active=True)
    return render(request, 'attendance/mark.html', {'employees': employees})

@login_required
def reports(request):
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)
    
    attendances = Attendance.objects.filter(
        date__month=month,
        date__year=year
    ).select_related('employee')
    
    return render(request, 'reports/index.html', {
        'attendances': attendances,
        'month': month,
        'year': year
    })

@login_required
def attendance_edit(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == 'POST':
        attendance.status = request.POST['status']
        check_in = request.POST.get('check_in', None)
        check_out = request.POST.get('check_out', None)
        attendance.check_in = check_in if check_in else None
        attendance.check_out = check_out if check_out else None
        attendance.remarks = request.POST.get('remarks', '')
        attendance.save()
        messages.success(request, 'Attendance updated successfully')
        return redirect('attendance_list')
    
    return render(request, 'attendance/edit.html', {'attendance': attendance})

@login_required
def attendance_delete(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance record deleted successfully')
    return redirect('attendance_list')
