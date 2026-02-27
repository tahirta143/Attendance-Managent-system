from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Users
    path('users/', views.users_list, name='users_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    
    # Roles
    path('roles/', views.roles_list, name='roles_list'),
    path('roles/create/', views.role_create, name='role_create'),
    path('roles/edit/<int:role_id>/', views.role_edit, name='role_edit'),
    path('roles/delete/<int:role_id>/', views.role_delete, name='role_delete'),
    
    # Permissions
    path('permissions/', views.permissions_list, name='permissions_list'),
    path('permissions/create/', views.permission_create, name='permission_create'),
    
    # User Roles
    path('user-roles/', views.user_roles, name='user_roles'),
    path('user-roles/assign/', views.assign_role, name='assign_role'),
    
    # Employees
    path('employees/', views.employees_list, name='employees_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/edit/<int:employee_id>/', views.employee_edit, name='employee_edit'),
    path('employees/delete/<int:employee_id>/', views.employee_delete, name='employee_delete'),
    
    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/edit/<int:attendance_id>/', views.attendance_edit, name='attendance_edit'),
    path('attendance/delete/<int:attendance_id>/', views.attendance_delete, name='attendance_delete'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
]
