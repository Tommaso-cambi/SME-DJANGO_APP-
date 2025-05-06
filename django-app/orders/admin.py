from django.contrib import admin
from .models import Customer, Supplier, Product, Order, OrderItem, PurchaseOrder, PurchaseOrderItem

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'city', 'country')
    list_filter = ('country', 'city')
    search_fields = ('name', 'contact_person', 'email', 'phone')
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'contact_person', 'email', 'phone', 'tax_id')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'city', 'country')
    list_filter = ('country', 'city')
    search_fields = ('name', 'contact_person', 'email', 'phone')
    fieldsets = (
        ('Supplier Information', {
            'fields': ('name', 'contact_person', 'email', 'phone', 'tax_id')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'cost', 'stock_quantity', 'main_supplier', 'is_active')
    list_filter = ('is_active', 'main_supplier')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('profit_margin',)
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'sku', 'description', 'main_supplier', 'image', 'is_active')
        }),
        ('Pricing', {
            'fields': ('price', 'cost', 'profit_margin')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'min_stock_level')
        }),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'quantity', 'unit_price', 'discount')
    autocomplete_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'date', 'status', 'total_amount', 'items_count')
    list_filter = ('status', 'date')
    search_fields = ('order_number', 'customer__name')
    inlines = [OrderItemInline]
    readonly_fields = ('total_amount', 'items_count')
    date_hierarchy = 'date'
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'order_number', 'date', 'status', 'employee')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country', 'shipping_cost')
        }),
        ('Financial Information', {
            'fields': ('tax_amount', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1
    fields = ('product', 'quantity', 'unit_cost')
    autocomplete_fields = ['product']

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'supplier', 'date', 'status', 'total_amount', 'items_count')
    list_filter = ('status', 'date')
    search_fields = ('po_number', 'supplier__name')
    inlines = [PurchaseOrderItemInline]
    readonly_fields = ('total_amount', 'items_count')
    date_hierarchy = 'date'
    fieldsets = (
        ('Purchase Order Information', {
            'fields': ('supplier', 'po_number', 'date', 'expected_delivery_date', 'status', 'employee')
        }),
        ('Financial Information', {
            'fields': ('shipping_cost', 'tax_amount', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )
