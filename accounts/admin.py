from django.contrib import admin
from .models import Role, Permission, RolePermission, UserRole, Employee, Attendance

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename', 'description']
    search_fields = ['name', 'codename']

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission']
    list_filter = ['role']

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'first_name', 'last_name', 'email', 'department', 'designation', 'is_active']
    list_filter = ['department', 'is_active', 'gender']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in', 'check_out', 'status']
    list_filter = ['status', 'date']
    search_fields = ['employee__employee_id', 'employee__first_name', 'employee__last_name']
    date_hierarchy = 'date'
