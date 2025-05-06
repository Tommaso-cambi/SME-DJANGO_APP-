from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Position(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions')
    salary_range_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_range_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.department.name}"
    
    class Meta:
        ordering = ['title']

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    EMPLOYMENT_STATUS = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CT', 'Contract'),
        ('IN', 'Intern')
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    hire_date = models.DateField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    employment_status = models.CharField(max_length=2, choices=EMPLOYMENT_STATUS, default='FT')
    emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']
        
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['employee', 'date']
        ordering = ['-date', 'employee']
    
    def __str__(self):
        return f"{self.employee} - {self.date}"

class Leave(models.Model):
    LEAVE_TYPES = [
        ('S', 'Sick'),
        ('V', 'Vacation'),
        ('P', 'Personal'),
        ('M', 'Maternity/Paternity'),
        ('O', 'Other')
    ]
    
    LEAVE_STATUS = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected')
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=1, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=LEAVE_STATUS, default='P')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee} - {self.get_leave_type_display()} ({self.start_date} to {self.end_date})"
    
    class Meta:
        ordering = ['-start_date']
