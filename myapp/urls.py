from django.contrib import admin
from django.urls import path
from . import views
from .views import (
    # Your existing views
    admin_dashboard,
    manage_products,
    add_product,
    edit_product,
    delete_product
)
urlpatterns = [
     
    path('admin/', admin.site.urls),
    
    # Home page
    path('', views.home_view, name='home'),
    
    # Product Listing
    path('products/', views.ProductListView.as_view(), name='product_list'),
    
    # Product Detail
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),


     # Admin-specific URLs
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/manage-products/', manage_products, name='manage_products'),
    path('admin/add-product/', add_product, name='add_product'),
    path('admin/edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('admin/delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('logout/', views.logout_view, name='logout'),

]