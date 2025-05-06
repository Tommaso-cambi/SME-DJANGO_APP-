from django.db import models
from django.utils import timezone
from employees.models import Employee

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5)
    main_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    class Meta:
        ordering = ['name']
    
    @property
    def profit_margin(self):
        if self.cost == 0:
            return 0
        return ((self.price - self.cost) / self.price) * 100
    
    @property
    def needs_restock(self):
        return self.stock_quantity <= self.min_stock_level

class Order(models.Model):
    ORDER_STATUS = [
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('X', 'Cancelled')
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='P')
    shipping_address = models.TextField(blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True, null=True)
    shipping_country = models.CharField(max_length=100, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.customer.name}"
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    @property
    def total_amount(self):
        total = sum(item.total_price for item in self.items.all())
        return total + self.shipping_cost + self.tax_amount
    
    @property
    def items_count(self):
        return self.items.count()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - Order #{self.order.order_number}"
    
    class Meta:
        ordering = ['id']
    
    @property
    def total_price(self):
        return (self.unit_price * self.quantity) - self.discount
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        # If creating a new order item, update product stock
        if is_new:
            self.product.stock_quantity -= self.quantity
            self.product.save()
        else:
            # If updating an existing order item, adjust stock based on quantity change
            old_order_item = OrderItem.objects.get(pk=self.pk)
            quantity_difference = self.quantity - old_order_item.quantity
            
            if quantity_difference != 0:
                self.product.stock_quantity -= quantity_difference
                self.product.save()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # When deleting an order item, restore the product stock
        self.product.stock_quantity += self.quantity
        self.product.save()
        
        super().delete(*args, **kwargs)

class PurchaseOrder(models.Model):
    PO_STATUS = [
        ('D', 'Draft'),
        ('S', 'Sent'),
        ('A', 'Approved'),
        ('R', 'Received'),
        ('C', 'Cancelled')
    ]
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders')
    po_number = models.CharField(max_length=50, unique=True)
    date = models.DateField(default=timezone.now)
    expected_delivery_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=PO_STATUS, default='D')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"PO #{self.po_number} - {self.supplier.name}"
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    @property
    def total_amount(self):
        total = sum(item.total_price for item in self.items.all())
        return total + self.shipping_cost + self.tax_amount
    
    @property
    def items_count(self):
        return self.items.count()

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_order_items')
    quantity = models.PositiveIntegerField(default=1)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - PO #{self.purchase_order.po_number}"
    
    class Meta:
        ordering = ['id']
    
    @property
    def total_price(self):
        return self.unit_cost * self.quantity
    
    def receive(self, received_quantity=None):
        # When items are received, update the product stock
        quantity_to_add = received_quantity if received_quantity is not None else self.quantity
        self.product.stock_quantity += quantity_to_add
        self.product.save()
        return quantity_to_add
