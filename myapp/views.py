from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views.generic import ListView
from .models import Product, Category, Discount,User, AdminAction
from django.utils import timezone
from django.db import connection


 
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
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.select_related('category').all()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        
        # Preserve category filter in pagination
        if 'category' in self.request.GET:
            context['pagination_query'] = f'category={self.request.GET["category"]}&'
        else:
            context['pagination_query'] = ''
        
        return context

def product_detail_view(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        product_id=product_id
    )
    
    related_products = (Product.objects
        .filter(category=product.category)
        .exclude(product_id=product.product_id)
        .select_related('category')[:4])

    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
        'has_image': bool(product.image)
    })



from django.http import JsonResponse
from .models import Category, Product, User, Profile, Discount, Cart, Wishlist, Order, Shipping, Payment, Review, SupportTicket, AdminAction



def get_categories(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT category_id, category_name FROM Category")
        categories = cursor.fetchall()
    return JsonResponse(categories, safe=False)

def get_products(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT p.product_id, p.product_name, p.description, p.price, p.stock_quantity, c.category_name 
            FROM Product p 
            JOIN Category c ON p.category_id = c.category_id
            """
        )
        products = cursor.fetchall()
    return JsonResponse(products, safe=False)

def get_users(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT user_id, username, email, role, registration_date FROM User")
        users = cursor.fetchall()
    return JsonResponse(users, safe=False)

def get_profiles(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT p.profile_id, u.username, p.address, p.phone, p.date_of_birth 
            FROM Profile p 
            JOIN User u ON p.user_id = u.user_id
            """
        )
        profiles = cursor.fetchall()
    return JsonResponse(profiles, safe=False)

def get_discounts(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT discount_id, discount_code, percentage, expiration_date FROM Discount")
        discounts = cursor.fetchall()
    return JsonResponse(discounts, safe=False)

def get_cart_items(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.cart_id, u.username, p.product_name, c.quantity 
            FROM Cart c 
            JOIN User u ON c.user_id = u.user_id 
            JOIN Product p ON c.product_id = p.product_id
            """
        )
        cart_items = cursor.fetchall()
    return JsonResponse(cart_items, safe=False)

def get_wishlist_items(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT w.wishlist_id, u.username, p.product_name 
            FROM Wishlist w 
            JOIN User u ON w.user_id = u.user_id 
            JOIN Product p ON w.product_id = p.product_id
            """
        )
        wishlist_items = cursor.fetchall()
    return JsonResponse(wishlist_items, safe=False)

def get_orders(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT o.order_id, u.username, o.order_date, o.status, o.total_amount 
            FROM Order o 
            JOIN User u ON o.user_id = u.user_id
            """
        )
        orders = cursor.fetchall()
    return JsonResponse(orders, safe=False)

def get_shipping_info(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT s.shipping_id, o.order_id, s.shipping_address, s.shipping_date, s.delivery_status 
            FROM Shipping s 
            JOIN Order o ON s.order_id = o.order_id
            """
        )
        shipping_info = cursor.fetchall()
    return JsonResponse(shipping_info, safe=False)

def get_payment_info(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT p.payment_id, o.order_id, p.payment_date, p.amount, p.payment_method 
            FROM Payment p 
            JOIN Order o ON p.order_id = o.order_id
            """
        )
        payment_info = cursor.fetchall()
    return JsonResponse(payment_info, safe=False)

def get_reviews(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT r.review_id, u.username, p.product_name, r.rating, r.review_text, r.review_date 
            FROM Review r 
            JOIN User u ON r.user_id = u.user_id 
            JOIN Product p ON r.product_id = p.product_id
            """
        )
        reviews = cursor.fetchall()
    return JsonResponse(reviews, safe=False)

def get_support_tickets(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT t.ticket_id, u.username, t.subject, t.message, t.status 
            FROM SupportTicket t 
            JOIN User u ON t.user_id = u.user_id
            """
        )
        support_tickets = cursor.fetchall()
    return JsonResponse(support_tickets, safe=False)

def get_admin_actions(request):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT a.action_id, u.username, a.action_description, a.action_date 
            FROM AdminAction a 
            JOIN User u ON a.admin_id = u.user_id
            """
        )
        admin_actions = cursor.fetchall()
    return JsonResponse(admin_actions, safe=False)

def action_button_view(request):
    return render(request, 'action_button.html')


def fetch_products_with_categories():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.product_id, p.product_name, p.price, c.category_name
            FROM Product p
            JOIN Category c ON p.category_id = c.category_id
        """)
        result = cursor.fetchall()
    return JsonResponse(result, safe=False)

def fetch_orders_with_users():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT o.order_id, o.order_date, u.username, u.email
            FROM Order o
            JOIN User u ON o.user_id = u.user_id
        """)
        result = cursor.fetchall()
    return JsonResponse(result, safe=False)

def fetch_reviews_with_products_and_users():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.review_id, r.rating, r.review_text, p.product_name, u.username
            FROM Review r
            JOIN Product p ON r.product_id = p.product_id
            JOIN User u ON r.user_id = u.user_id
        """)
        result = cursor.fetchall()
    return JsonResponse(result, safe=False)

def fetch_cart_items_with_user_and_product():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.cart_id, u.username, p.product_name, c.quantity
            FROM Cart c
            JOIN User u ON c.user_id = u.user_id
            JOIN Product p ON c.product_id = p.product_id
        """)
        result = cursor.fetchall()
    return JsonResponse(result, safe=False)
def fetch_users_with_most_expensive_cart_item():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.username, u.email, c.product_id, p.product_name, p.price
            FROM User u
            JOIN Cart c ON u.user_id = c.user_id
            JOIN Product p ON c.product_id = p.product_id
            WHERE p.price = (
                SELECT MAX(p2.price)
                FROM Cart c2
                JOIN Product p2 ON c2.product_id = p2.product_id
                WHERE c2.user_id = u.user_id
            )
        """)
        result = cursor.fetchall()
    return JsonResponse(result, safe=False)

def fetch_category_with_most_products():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.category_name, COUNT(p.product_id) AS product_count
            FROM Category c
            JOIN Product p ON c.category_id = p.category_id
            WHERE c.category_id = (
                SELECT category_id
                FROM Product
                GROUP BY category_id
                ORDER BY COUNT(product_id) DESC
                LIMIT 1
            )
            GROUP BY c.category_name
        """)
        result = cursor.fetchall()
    return JsonResponse(result, safe=False)

def fetch_user_with_most_orders():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.username, u.email, COUNT(o.order_id) AS order_count
            FROM User u
            JOIN Order o ON u.user_id = o.user_id
            WHERE u.user_id = (
                SELECT user_id
                FROM Order
                GROUP BY user_id
                ORDER BY COUNT(order_id) DESC
                LIMIT 1
            )
            GROUP BY u.username, u.email
        """)
        result = cursor.fetchall()
    return JsonResponse(result, safe=False)

def fetch_products_with_high_ratings():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.product_id, p.product_name, AVG(r.rating) AS avg_rating
            FROM Product p
            JOIN Review r ON p.product_id = r.product_id
            WHERE p.product_id IN (
                SELECT product_id
                FROM Review
                GROUP BY product_id
                HAVING AVG(rating) > 4
            )
            GROUP BY p.product_id, p.product_name
        """)
        result = cursor.fetchall()
    return JsonResponse(result, safe=False)













# View to fetch all categories
def get_categories(request):
    categories = Category.objects.all().values('category_id', 'category_name')
    return JsonResponse(list(categories), safe=False)

# View to fetch all products
def get_products(request):
    products = Product.objects.all().values('product_id', 'product_name', 'description', 'price', 'stock_quantity', 'category__category_name')
    return JsonResponse(list(products), safe=False)

# View to fetch all users
def get_users(request):
    users = User.objects.all().values('user_id', 'username', 'email', 'role', 'registration_date')
    return JsonResponse(list(users), safe=False)

# View to fetch all profiles
def get_profiles(request):
    profiles = Profile.objects.all().values('profile_id', 'user__username', 'address', 'phone', 'date_of_birth')
    return JsonResponse(list(profiles), safe=False)

# View to fetch all discounts
def get_discounts(request):
    discounts = Discount.objects.all().values('discount_id', 'discount_code', 'percentage', 'expiration_date')
    return JsonResponse(list(discounts), safe=False)

# View to fetch all cart items
def get_cart_items(request):
    cart_items = Cart.objects.all().values('cart_id', 'user__username', 'product__product_name', 'quantity')
    return JsonResponse(list(cart_items), safe=False)

# View to fetch all wishlist items
def get_wishlist_items(request):
    wishlist_items = Wishlist.objects.all().values('wishlist_id', 'user__username', 'product__product_name')
    return JsonResponse(list(wishlist_items), safe=False)

# View to fetch all orders
def get_orders(request):
    orders = Order.objects.all().values('order_id', 'user__username', 'order_date', 'status', 'total_amount')
    return JsonResponse(list(orders), safe=False)

# View to fetch all shipping info
def get_shipping_info(request):
    shipping_info = Shipping.objects.all().values('shipping_id', 'order__order_id', 'shipping_address', 'shipping_date', 'delivery_status')
    return JsonResponse(list(shipping_info), safe=False)

# View to fetch all payment info
def get_payment_info(request):
    payment_info = Payment.objects.all().values('payment_id', 'order__order_id', 'payment_date', 'amount', 'payment_method')
    return JsonResponse(list(payment_info), safe=False)

# View to fetch all reviews
def get_reviews(request):
    reviews = Review.objects.all().values('review_id', 'user__username', 'product__product_name', 'rating', 'review_text', 'review_date')
    return JsonResponse(list(reviews), safe=False)

# View to fetch all support tickets
def get_support_tickets(request):
    support_tickets = SupportTicket.objects.all().values('ticket_id', 'user__username', 'subject', 'message', 'status')
    return JsonResponse(list(support_tickets), safe=False)

# View to fetch all admin actions
def get_admin_actions(request):
    admin_actions = AdminAction.objects.all().values('action_id', 'admin__username', 'action_description', 'action_date')
    return JsonResponse(list(admin_actions), safe=False)


def action_button_view(request):
    return render(request, 'action_button.html')


from django.shortcuts import render

def search_products(request):
  """
  This view function handles product searches based on a search term.
  """
  query = request.GET.get('q', '')  # Get the search query from the URL parameter
  if query:
    products = Product.objects.filter(product_name__icontains=query)  # Filter products by name (case-insensitive)
  else:
    products = Product.objects.all()  # If no query provided, return all products
  context = {'products': products, 'query': query}
  return render(request, 'search_results.html', context)