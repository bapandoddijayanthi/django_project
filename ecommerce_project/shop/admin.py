from django.contrib import admin
from .models import Category, Product, Order, OrderItem

# Register Category model with custom display options
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # Automatically populate slug from name

# Register Product model with custom display options
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available'] # Allow editing directly from list view
    prepopulated_fields = {'slug': ('name',)} # Automatically populate slug from name

# Inline for OrderItems within the Order admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product'] # Use a raw ID input for product selection

# Register Order model with custom display options
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline] # Include OrderItems inline

