from django.contrib import admin
from .models import Category, Account, Transaction, Budget

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    list_filter = ('type',)
    search_fields = ('name', 'description')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'bank_name', 'current_balance')
    list_filter = ('account_type',)
    search_fields = ('name', 'bank_name', 'account_number')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'date', 'amount', 'category', 'account', 'description', 'payment_method')
    list_filter = ('transaction_type', 'date', 'category', 'account', 'payment_method')
    search_fields = ('description', 'reference_number')
    date_hierarchy = 'date'
    fieldsets = (
        ('Transaction Details', {
            'fields': ('transaction_type', 'date', 'amount', 'category', 'account', 'description')
        }),
        ('Payment Information', {
            'fields': ('reference_number', 'payment_method', 'recorded_by', 'receipt_image')
        }),
    )

admin.site.register(Transaction, TransactionAdmin)

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'period', 'start_date', 'end_date')
    list_filter = ('period', 'start_date', 'category')
    search_fields = ('category__name', 'notes')
    date_hierarchy = 'start_date'
