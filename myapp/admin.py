from django.contrib import admin

# Register your models here.
 
from .models import (
    Category, Product, User, Profile, Discount, 
    Cart, Wishlist, Order, OrderItem, SupportTicket, 
    AdminAction, Review, Shipping, Payment, OrderDiscount
)

# Basic admin registration for all models
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Discount)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(SupportTicket)
admin.site.register(AdminAction)
admin.site.register(Review)
admin.site.register(Shipping)
admin.site.register(Payment)
admin.site.register(OrderDiscount)