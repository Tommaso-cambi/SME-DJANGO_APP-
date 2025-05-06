from django.shortcuts import render
from .models import Customer, Supplier, Product, Order, PurchaseOrder
from django.db.models import F

# Create your views here.
def orders_dashboard(request):
    customer_orders = Order.objects.all().order_by('-date')[:10]
    purchase_orders = PurchaseOrder.objects.all().order_by('-date')[:10]
    customers = Customer.objects.all()[:5]
    suppliers = Supplier.objects.all()[:5]
    
    # Get products that need to be reordered
    low_stock_products = Product.objects.filter(stock_quantity__lte=F('min_stock_level'))
    
    context = {
        'customer_orders': customer_orders,
        'purchase_orders': purchase_orders,
        'customers': customers,
        'suppliers': suppliers,
        'low_stock_products': low_stock_products,
        'customer_orders_count': Order.objects.count(),
        'supplier_orders_count': PurchaseOrder.objects.count(),
        'products_count': Product.objects.count(),
        'products_to_reorder': low_stock_products.count(),
    }
    
    return render(request, 'orders/orders_dashboard.html', context)
