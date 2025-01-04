from django.db import models

# Create your models here.
 
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    stock_quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # Image field added

    def __str__(self):
        return self.product_name


class User(models.Model):
    ROLE_CHOICES = [
        ('Customer', 'Customer'),
        ('Admin', 'Admin')
    ]
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    registration_date = models.DateField()
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    discount_code = models.CharField(max_length=50, unique=True)
    percentage = models.FloatField()
    expiration_date = models.DateField()

    def __str__(self):
        return self.discount_code

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField()
    status = models.CharField(max_length=50, null=True, blank=True)
    total_amount = models.FloatField()

class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

class SupportTicket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=50)

class AdminAction(models.Model):
    action_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    action_description = models.TextField()
    action_date = models.DateField()

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField(null=True, blank=True)
    review_date = models.DateField()

class Shipping(models.Model):
    shipping_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    shipping_date = models.DateField()
    delivery_status = models.CharField(max_length=50)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50)

class OrderDiscount(models.Model):
    order_discount_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)