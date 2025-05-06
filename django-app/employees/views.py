from django.shortcuts import render
from .models import Department, Position, Employee, Attendance, Leave

# Create your views here.
def employee_list(request):
    employees = Employee.objects.all()
    departments = Department.objects.all()
    positions = Position.objects.all()
    
    context = {
        'employees': employees,
        'departments': departments,
        'positions': positions,
    }
    
    return render(request, 'employees/employees_list.html', context)
