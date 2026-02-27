from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('role', 'permission')
    
    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name if self.role else 'No Role'}"

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = self.generate_employee_id()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_employee_id():
        """Generate unique employee ID in format EMP001, EMP002, etc."""
        last_employee = Employee.objects.all().order_by('id').last()
        if not last_employee or not last_employee.employee_id:
            return 'EMP001'
        
        # Extract number from last employee_id
        last_id = last_employee.employee_id
        if last_id.startswith('EMP'):
            try:
                last_number = int(last_id[3:])
                new_number = last_number + 1
                return f'EMP{new_number:03d}'
            except ValueError:
                pass
        
        # Fallback: count all employees and add 1
        count = Employee.objects.count()
        return f'EMP{count + 1:03d}'
    
    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
        ('late', 'Late'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"
