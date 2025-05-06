from django.shortcuts import render
from .models import Category, Account, Transaction, Budget
from django.db.models import Sum

# Create your views here.
def finances_dashboard(request):
    transactions = Transaction.objects.all().order_by('-date')[:10]
    accounts = Account.objects.all()
    categories = Category.objects.all()
    
    # Calculate totals
    income_total = Transaction.objects.filter(transaction_type='I').aggregate(total=Sum('amount'))
    expense_total = Transaction.objects.filter(transaction_type='E').aggregate(total=Sum('amount'))
    
    total_income = income_total['total'] or 0
    total_expenses = expense_total['total'] or 0
    balance = total_income - total_expenses
    
    context = {
        'transactions': transactions,
        'accounts': accounts,
        'categories': categories,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'accounts_count': accounts.count(),
    }
    
    return render(request, 'finances/finances_dashboard.html', context)
