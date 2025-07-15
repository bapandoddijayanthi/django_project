from django.urls import path
from . import views

app_name = 'shop' # Namespace for URLs

urlpatterns = [
    # Specific URLs should come first
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('order/create/', views.order_create, name='order_create'),

    # Product detail (also more specific than category slug)
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # General product list and category list should come last
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('', views.product_list, name='product_list'), # This should generally be the last catch-all for the app root
]