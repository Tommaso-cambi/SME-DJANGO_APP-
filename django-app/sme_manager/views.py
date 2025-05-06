from django.shortcuts import render
from employees.models import Employee
from finances.models import Transaction
from orders.models import Order
from django.db.models import Sum
from django.utils import timezone
import datetime

def index(request):
    # Get counts for dashboard
    employee_count = Employee.objects.count()
    
    # Get current month data
    today = timezone.now()
    month_start = datetime.date(today.year, today.month, 1)
    
    # Get monthly income and expenses
    income_month = Transaction.objects.filter(
        transaction_type='I',
        date__gte=month_start,
        date__lte=today
    ).aggregate(total=Sum('amount'))
    
    expense_month = Transaction.objects.filter(
        transaction_type='E',
        date__gte=month_start,
        date__lte=today
    ).aggregate(total=Sum('amount'))
    
    # Get pending orders
    pending_orders = Order.objects.filter(status='P').count()
    
    # Get recent data for dashboard
    recent_employees = Employee.objects.all().order_by('-hire_date')[:5]
    recent_orders = Order.objects.all().order_by('-date')[:5]
    recent_transactions = Transaction.objects.all().order_by('-date')[:10]
    
    context = {
        'employee_count': employee_count,
        'income_month': income_month['total'] or 0,
        'expense_month': expense_month['total'] or 0,
        'pending_orders': pending_orders,
        'recent_employees': recent_employees,
        'recent_orders': recent_orders,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'index.html', context)
