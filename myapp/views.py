from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views.generic import ListView
from .models import Product, Category, Discount,User, AdminAction
from django.utils import timezone


 
from django.contrib import messages
 
from django.db.models import Count
 

# Create your views here.

 

def HomeScreen(request):
    context = {
        'greeting': 'Hello, Django!'
    }
    return render(request, 'homescreen.html', context)



def home_view(request):
    """
    Home view to display featured products, categories, and active discounts
    """
    # Get featured products (top 8 products sorted by some criteria)
    featured_products = Product.objects.order_by('-product_id')[:8]
    
    # Get all categories
    categories = Category.objects.all()
    
    # Get active discounts
    
    active_discounts = Discount.objects.filter(expiration_date__gte=timezone.now())
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'active_discounts': active_discounts
    }
    
    return render(request, 'homescreen.html', context)

class ProductListView(ListView):
    """
    View to list products, optionally filtered by category
    """
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        # Filter products by category if category_id is provided
        queryset = Product.objects.all()
        category_id = self.request.GET.get('category')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def product_detail_view(request, product_id):
    """
    View to show detailed information about a specific product
    """
    product = Product.objects.get(product_id=product_id)
    
    # Get related products from the same category
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(product_id=product.product_id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    
    return render(request, 'product_detail.html', context)






#Admin site

def admin_dashboard(request):
    """
    Dashboard for admin users to view key statistics and perform management
    """
    # Check if the current user is an admin
    try:
        user = User.objects.get(username=request.user.username, role='Admin')
    except User.DoesNotExist:
        messages.error(request, "Access Denied. Admin rights required.")
        return redirect('home')

    # Collect dashboard statistics
    product_stats = Product.objects.values('category__category_name') \
        .annotate(product_count=Count('product_id'))
    
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock_quantity__lte=10)
    categories = Category.objects.all()

    # Log admin dashboard access
    AdminAction.objects.create(
        admin=user,
        action_description="Accessed Admin Dashboard",
        action_date=timezone.now()
    )

    context = {
        'product_stats': product_stats,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'categories': categories
    }
    return render(request, 'admin/dashboard.html', context)

def manage_products(request):
    """
    View to list and manage all products
    """
    # Check admin rights
    try:
        user = User.objects.get(username=request.user.username, role='Admin')
    except User.DoesNotExist:
        messages.error(request, "Access Denied. Admin rights required.")
        return redirect('home')

    # Get all products with category information
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    # Log product management access
    AdminAction.objects.create(
        admin=user,
        action_description="Accessed Product Management",
        action_date=timezone.now()
    )

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'admin/manage_products.html', context)

def logout_view(request):
    logout(request)
    return redirect('home') 

def add_product(request):
    """
    View to add a new product
    """
    # Check admin rights
    try:
        user = User.objects.get(username=request.user.username, role='Admin')
    except User.DoesNotExist:
        messages.error(request, "Access Denied. Admin rights required.")
        return redirect('home')

    if request.method == 'POST':
        # Extract form data
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        category_id = request.POST.get('category')

        # Validate input
        if not all([product_name, price, stock_quantity, category_id]):
            messages.error(request, "Please fill all required fields.")
            return redirect('add_product')

        try:
            category = Category.objects.get(category_id=category_id)
            
            # Create new product
            Product.objects.create(
                product_name=product_name,
                description=description,
                price=float(price),
                stock_quantity=int(stock_quantity),
                category=category
            )

            # Log admin action
            AdminAction.objects.create(
                admin=user,
                action_description=f"Added new product: {product_name}",
                action_date=timezone.now()
            )

            messages.success(request, "Product added successfully!")
            return redirect('manage_products')

        except (ValueError, Category.DoesNotExist):
            messages.error(request, "Invalid input. Please check your data.")
            return redirect('add_product')

    categories = Category.objects.all()
    return render(request, 'admin/add_product.html', {'categories': categories})

def edit_product(request, product_id):
    """
    View to edit an existing product
    """
    # Check admin rights
    try:
        user = User.objects.get(username=request.user.username, role='Admin')
    except User.DoesNotExist:
        messages.error(request, "Access Denied. Admin rights required.")
        return redirect('home')

    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        # Extract form data
        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('description')
        product.price = float(request.POST.get('price'))
        product.stock_quantity = int(request.POST.get('stock_quantity'))
        
        category_id = request.POST.get('category')
        product.category = Category.objects.get(category_id=category_id)

        product.save()

        # Log admin action
        AdminAction.objects.create(
            admin=user,
            action_description=f"Updated product: {product.product_name}",
            action_date=timezone.now()
        )

        messages.success(request, "Product updated successfully!")
        return redirect('manage_products')

    categories = Category.objects.all()
    return render(request, 'admin/edit_product.html', {
        'product': product, 
        'categories': categories
    })

def delete_product(request, product_id):
    """
    View to delete a product
    """
    # Check admin rights
    try:
        user = User.objects.get(username=request.user.username, role='Admin')
    except User.DoesNotExist:
        messages.error(request, "Access Denied. Admin rights required.")
        return redirect('home')

    product = get_object_or_404(Product, product_id=product_id)
    
    # Log admin action before deletion
    AdminAction.objects.create(
        admin=user,
        action_description=f"Deleted product: {product.product_name}",
        action_date=timezone.now()
    )

    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('manage_products')