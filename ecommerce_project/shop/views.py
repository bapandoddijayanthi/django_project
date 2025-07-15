from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Order, OrderItem
from .forms import CartAddProductForm, OrderCreateForm
from .cart import Cart # Import the Cart class

# Product list view
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product_list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

# Product detail view
def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm() # Form to add product to cart
    return render(request,
                  'shop/product_detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

# Cart Add view
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('shop:cart_detail')

# Cart Remove view
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

# Cart Detail view
def cart_detail(request):
    cart = Cart(request)
    # Update quantities for items in the cart if needed
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={'quantity': item['quantity'],
                                                 'update': True})
    return render(request, 'shop/cart_detail.html', {'cart': cart})

# Order Creation View
def order_create(request):
    cart = Cart(request)
    if not cart:
        # Redirect if cart is empty
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save() # Save the order instance

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # For simplicity, we'll just redirect to a success page or product list
            # In a real app, you'd integrate payment here and then redirect
            # For now, let's just mark it as paid for demonstration
            order.paid = True
            order.save()
            return render(request, 'shop/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'shop/order_create.html', {'cart': cart, 'form': form})

