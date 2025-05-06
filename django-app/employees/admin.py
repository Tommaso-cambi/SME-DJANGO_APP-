from django.contrib import admin
from .models import Department, Position, Employee, Attendance, Leave

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'salary_range_min', 'salary_range_max')
    list_filter = ('department',)
    search_fields = ('title', 'department__name')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'position', 'department', 'employment_status', 'hire_date')
    list_filter = ('department', 'position', 'employment_status')
    search_fields = ('first_name', 'last_name', 'email')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'date_of_birth', 'gender')
        }),
        ('Employment Details', {
            'fields': ('hire_date', 'position', 'department', 'salary', 'employment_status')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'time_in', 'time_out')
    list_filter = ('date', 'employee__department')
    search_fields = ('employee__first_name', 'employee__last_name', 'date')
    date_hierarchy = 'date'

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter = ('leave_type', 'status', 'start_date')
    search_fields = ('employee__first_name', 'employee__last_name')
    date_hierarchy = 'start_date'
