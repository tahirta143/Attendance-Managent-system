from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q, Count
from .models import Role, Permission, RolePermission, UserRole, Employee, Attendance
from .serializers import (
    UserSerializer, RoleSerializer, PermissionSerializer,
    RolePermissionSerializer, UserRoleSerializer, EmployeeSerializer,
    AttendanceSerializer, DashboardStatsSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users
    """
    queryset = User.objects.all().select_related('user_role__role')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        return queryset

class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for roles
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for permissions
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

class RolePermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for role permissions
    """
    queryset = RolePermission.objects.all().select_related('role', 'permission')
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated]

class UserRoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user roles
    """
    queryset = UserRole.objects.all().select_related('user', 'role')
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for employees
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        department = self.request.query_params.get('department', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if search:
            queryset = queryset.filter(
                Q(employee_id__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def departments(self, request):
        """Get list of unique departments"""
        departments = Employee.objects.values_list('department', flat=True).distinct()
        return Response({'departments': list(departments)})
    
    @action(detail=False, methods=['get'])
    def next_id(self, request):
        """Get next employee ID"""
        next_id = Employee.generate_employee_id()
        return Response({'next_employee_id': next_id})

class AttendanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for attendance
    """
    queryset = Attendance.objects.all().select_related('employee')
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date', None)
        employee_id = self.request.query_params.get('employee_id', None)
        status_filter = self.request.query_params.get('status', None)
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)
        
        is_employee = hasattr(self.request.user, 'user_role') and self.request.user.user_role.role and self.request.user.user_role.role.name.lower() == 'employee'
        if is_employee:
            queryset = queryset.filter(employee__email=self.request.user.email)
        
        if date:
            queryset = queryset.filter(date=date)
        
        if employee_id and not is_employee:
            queryset = queryset.filter(employee__employee_id=employee_id)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        if month and year:
            queryset = queryset.filter(date__month=month, date__year=year)
        
        return queryset.order_by('-date')
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's attendance"""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(date=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get attendance summary for a date"""
        date = request.query_params.get('date', timezone.now().date())
        
        summary = Attendance.objects.filter(date=date).values('status').annotate(
            count=Count('id')
        )
        
        result = {item['status']: item['count'] for item in summary}
        result['date'] = date
        result['total'] = sum(result.values()) if isinstance(result, dict) else 0
        
        return Response(result)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics
    """
    from datetime import timedelta
    today = timezone.now().date()
    
    # Check if user is employee
    is_employee = hasattr(request.user, 'user_role') and request.user.user_role.role and request.user.user_role.role.name.lower() == 'employee'
    
    if is_employee:
        total_employees = 1
        present_today = Attendance.objects.filter(date=today, status='present', employee__email=request.user.email).count()
        absent_today = Attendance.objects.filter(date=today, status='absent', employee__email=request.user.email).count()
        leave_today = Attendance.objects.filter(date=today, status='leave', employee__email=request.user.email).count()
        late_today = Attendance.objects.filter(date=today, status='late', employee__email=request.user.email).count()
        
        weekly_data = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            day_data = {
                'date': date.strftime('%Y-%m-%d'),
                'present': Attendance.objects.filter(date=date, status='present', employee__email=request.user.email).count(),
                'absent': Attendance.objects.filter(date=date, status='absent', employee__email=request.user.email).count(),
                'leave': Attendance.objects.filter(date=date, status='leave', employee__email=request.user.email).count(),
                'late': Attendance.objects.filter(date=date, status='late', employee__email=request.user.email).count(),
            }
            weekly_data.append(day_data)
        
        employee = Employee.objects.filter(email=request.user.email).first()
        dept_attendance = []
        if employee:
            dept_attendance = [{
                'department': employee.department,
                'present': present_today
            }]
    else:
        total_employees = Employee.objects.filter(is_active=True).count()
        present_today = Attendance.objects.filter(date=today, status='present').count()
        absent_today = Attendance.objects.filter(date=today, status='absent').count()
        leave_today = Attendance.objects.filter(date=today, status='leave').count()
        late_today = Attendance.objects.filter(date=today, status='late').count()
        
        # Weekly data (last 7 days)
        weekly_data = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
        day_data = {
            'date': date.strftime('%Y-%m-%d'),
            'present': Attendance.objects.filter(date=date, status='present').count(),
            'absent': Attendance.objects.filter(date=date, status='absent').count(),
            'leave': Attendance.objects.filter(date=date, status='leave').count(),
            'late': Attendance.objects.filter(date=date, status='late').count(),
        }
        weekly_data.append(day_data)
    
    if not is_employee:
        dept_attendance = []
        # Department-wise attendance for today
        departments = Employee.objects.values('department').distinct()
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
    
    # Department weekly attendance (for new chart)
    dept_weekly_data = []
    if not is_employee:
        departments_list = Employee.objects.values_list('department', flat=True).distinct()
        for dept_name in departments_list:
            
            dept_week = {'department': dept_name, 'data': []}
            for i in range(6, -1, -1):
                d = today - timedelta(days=i)
                dept_present = Attendance.objects.filter(
                    date=d,
                    status='present',
                    employee__department=dept_name
                ).count()
                dept_week['data'].append(dept_present)
            dept_weekly_data.append(dept_week)
            
    data = {
        'total_employees': total_employees,
        'present_today': present_today,
        'absent_today': absent_today,
        'leave_today': leave_today,
        'late_today': late_today,
        'date': today,
        'weekly_data': weekly_data,
        'dept_attendance': dept_attendance,
        'dept_weekly_data': dept_weekly_data,
    }
    
    # We're bypassing the serializer to return the extra dynamic field easily
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_report(request):
    """
    Get attendance report with filters
    """
    month = request.query_params.get('month', timezone.now().month)
    year = request.query_params.get('year', timezone.now().year)
    employee_id = request.query_params.get('employee_id', None)
    
    queryset = Attendance.objects.filter(
        date__month=month,
        date__year=year
    ).select_related('employee')
    
    # Restrict to own data if user is an employee
    is_employee = hasattr(request.user, 'user_role') and request.user.user_role.role and request.user.user_role.role.name.lower() == 'employee'
    if is_employee:
        queryset = queryset.filter(employee__email=request.user.email)
    elif employee_id:
        queryset = queryset.filter(employee__employee_id=employee_id)
    
    # Group by employee
    report = {}
    for attendance in queryset:
        emp_id = attendance.employee.employee_id
        if emp_id not in report:
            report[emp_id] = {
                'employee_id': emp_id,
                'employee_name': f"{attendance.employee.first_name} {attendance.employee.last_name}",
                'department': attendance.employee.department,
                'present': 0,
                'absent': 0,
                'leave': 0,
                'late': 0,
                'total_days': 0
            }
        
        report[emp_id][attendance.status] += 1
        report[emp_id]['total_days'] += 1
    
    return Response({
        'month': month,
        'year': year,
        'report': list(report.values())
    })


# Authentication Views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user info"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom claims
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        
        # Add role if exists
        try:
            if hasattr(self.user, 'user_role') and self.user.user_role.role:
                data['role'] = self.user.user_role.role.name
        except:
            data['role'] = None
        
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view"""
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    Login API endpoint
    
    POST /api/auth/login/
    {
        "username": "admin",
        "password": "admin123"
    }
    
    Returns:
    {
        "access": "token...",
        "refresh": "token...",
        "user_id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "Administrator"
    }
    """
    from rest_framework_simplejwt.tokens import RefreshToken
    from django.contrib.auth import authenticate
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.is_active:
        return Response(
            {'error': 'User account is disabled'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
    # Get user role
    role = None
    try:
        if hasattr(user, 'user_role') and user.user_role.role:
            role = user.user_role.role.name
    except:
        pass
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': role,
        'message': 'Login successful'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """
    Logout API endpoint
    
    POST /api/auth/logout/
    {
        "refresh": "refresh_token_here"
    }
    """
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
        
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Logout successful'
        })
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_user_profile(request):
    """
    Get current user profile
    
    GET /api/auth/profile/
    """
    user = request.user
    
    # Get user role
    role = None
    try:
        if hasattr(user, 'user_role') and user.user_role.role:
            role = user.user_role.role.name
    except:
        pass
    
    return Response({
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined,
        'role': role
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def api_refresh_token(request):
    """
    Refresh access token
    
    POST /api/auth/refresh/
    {
        "refresh": "refresh_token_here"
    }
    """
    from rest_framework_simplejwt.tokens import RefreshToken
    
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        return Response(
            {'error': 'Refresh token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token)
        })
    except Exception as e:
        return Response(
            {'error': 'Invalid refresh token'},
            status=status.HTTP_401_UNAUTHORIZED
        )
