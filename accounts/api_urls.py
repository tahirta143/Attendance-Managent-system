from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    UserViewSet, RoleViewSet, PermissionViewSet,
    RolePermissionViewSet, UserRoleViewSet, EmployeeViewSet,
    AttendanceViewSet, dashboard_stats, attendance_report,
    api_login, api_logout, api_user_profile, api_refresh_token
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='api-users')
router.register(r'roles', RoleViewSet, basename='api-roles')
router.register(r'permissions', PermissionViewSet, basename='api-permissions')
router.register(r'role-permissions', RolePermissionViewSet, basename='api-role-permissions')
router.register(r'user-roles', UserRoleViewSet, basename='api-user-roles')
router.register(r'employees', EmployeeViewSet, basename='api-employees')
router.register(r'attendance', AttendanceViewSet, basename='api-attendance')

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', api_login, name='api-login'),
    path('auth/logout/', api_logout, name='api-logout'),
    path('auth/profile/', api_user_profile, name='api-profile'),
    path('auth/refresh/', api_refresh_token, name='api-refresh'),
    
    # Data endpoints
    path('dashboard/stats/', dashboard_stats, name='api-dashboard-stats'),
    path('reports/attendance/', attendance_report, name='api-attendance-report'),
    
    # Router URLs
    path('', include(router.urls)),
]
