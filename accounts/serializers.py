from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, Permission, RolePermission, UserRole, Employee, Attendance

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'role']
        read_only_fields = ['date_joined']
    
    def get_role(self, obj):
        try:
            return obj.user_role.role.name if obj.user_role.role else None
        except:
            return None

class RoleSerializer(serializers.ModelSerializer):
    permissions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'created_at', 'permissions_count']
        read_only_fields = ['created_at']
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'description']

class RolePermissionSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    permission_name = serializers.CharField(source='permission.name', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'role_name', 'permission', 'permission_name']

class UserRoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'username', 'role', 'role_name']

class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'gender', 'gender_display',
            'date_of_birth', 'date_of_joining', 'department', 'designation',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['employee_id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    employee_id_display = serializers.CharField(source='employee.employee_id', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_id_display', 'employee_name',
            'date', 'check_in', 'check_out', 'status', 'status_display',
            'remarks', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"

class DashboardStatsSerializer(serializers.Serializer):
    total_employees = serializers.IntegerField()
    present_today = serializers.IntegerField()
    absent_today = serializers.IntegerField()
    leave_today = serializers.IntegerField()
    late_today = serializers.IntegerField()
    date = serializers.DateField()
    weekly_data = serializers.ListField(child=serializers.DictField())
    dept_attendance = serializers.ListField(child=serializers.DictField())
