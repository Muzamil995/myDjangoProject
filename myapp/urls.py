from django.contrib import admin
from django.urls import path
from . import views
 

app_name = "action"
urlpatterns = [
     
 
    
    # Home page
    path('', views.home_view, name='home'),
    
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),


    path('action-button/', views.action_button_view, name='action-button'),

    path('get-categories/', views.get_categories, name='get-categories'),
    path('get-products/', views.get_products, name='get-products'),
    path('get-users/', views.get_users, name='get-users'),
    path('get-profiles/', views.get_profiles, name='get-profiles'),
    path('get-discounts/', views.get_discounts, name='get-discounts'),
    path('get-cart-items/', views.get_cart_items, name='get-cart_items'),
    path('get-wishlist-items/', views.get_wishlist_items, name='get-wishlist_items'),
    path('get-orders/', views.get_orders, name='get_orders'),
    path('get-shipping-info/', views.get_shipping_info, name='get-shipping_info'),
    path('get-payment-info/', views.get_payment_info, name='get-payment_info'),
    path('get-reviews/', views.get_reviews, name='get-reviews'),
    path('get-support-tickets/', views.get_support_tickets, name='get-support-tickets'),
    path('get-admin-actions/', views.get_admin_actions, name='get-admin-actions'),


     
   

]