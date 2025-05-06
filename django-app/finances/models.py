from django.db import models
from django.utils import timezone
from employees.models import Employee

# Create your models here.
class Category(models.Model):
    CATEGORY_TYPES = [
        ('I', 'Income'),
        ('E', 'Expense')
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['type', 'name']

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('C', 'Cash'),
        ('B', 'Bank Account'),
        ('CC', 'Credit Card'),
        ('O', 'Other')
    ]
    
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPES)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('I', 'Income'),
        ('E', 'Expense')
    ]
    
    PAYMENT_METHODS = [
        ('CA', 'Cash'),
        ('BT', 'Bank Transfer'),
        ('CC', 'Credit Card'),
        ('CH', 'Check'),
        ('OL', 'Online Payment'),
        ('OT', 'Other')
    ]
    
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    description = models.TextField()
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHODS, default='CA')
    recorded_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='recorded_transactions')
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} - {self.date}"
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def save(self, *args, **kwargs):
        # Update account balance
        is_new = self.pk is None
        
        if not is_new:
            # If updating an existing transaction, first revert its effect
            old_transaction = Transaction.objects.get(pk=self.pk)
            if old_transaction.transaction_type == 'I':
                old_transaction.account.current_balance -= old_transaction.amount
            else:
                old_transaction.account.current_balance += old_transaction.amount
            old_transaction.account.save()
        
        # Apply the new transaction effect
        if self.transaction_type == 'I':
            self.account.current_balance += self.amount
        else:
            self.account.current_balance -= self.amount
        self.account.save()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # When a transaction is deleted, update the account balance
        if self.transaction_type == 'I':
            self.account.current_balance -= self.amount
        else:
            self.account.current_balance += self.amount
        self.account.save()
        
        super().delete(*args, **kwargs)

class Budget(models.Model):
    BUDGET_PERIODS = [
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('Y', 'Yearly')
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    period = models.CharField(max_length=1, choices=BUDGET_PERIODS, default='M')
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.category.name} Budget - {self.get_period_display()} ({self.start_date} to {self.end_date})"
    
    class Meta:
        ordering = ['-start_date', 'category']
