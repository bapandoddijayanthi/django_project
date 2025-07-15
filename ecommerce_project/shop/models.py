from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User # Using Django's built-in User model

# Category model to organize products
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True) # For clean URLs

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    # Method to get the URL for a specific category
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

# Product model
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True) # For clean URLs
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True) # Image field
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # For currency
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        # Corrected: Use 'indexes' instead of 'index_together' for modern Django versions
        # Define a database index on 'id' and 'slug' for efficient lookups
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        return self.name

    # Method to get the URL for a specific product
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

# Order model
class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True, blank=True) # Can be null for guest checkout
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False) # To track payment status

    class Meta:
        ordering = ('-created',) # Order by creation date, newest first

    def __str__(self):
        return f'Order {self.id}'

    # Method to calculate the total cost of the order
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

# OrderItem model (items within an order)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    # Method to calculate the cost for this specific item (price * quantity)
    def get_cost(self):
        return self.price * self.quantity

