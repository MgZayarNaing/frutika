from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *

# Add product to cart view
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_detail')

# Cart detail view
@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    subtotal = sum(item.total_price() for item in cart_items)
    shipping = 45  # Example shipping cost
    total = subtotal + shipping
    if cart.coupon:
        total -= cart.coupon.discount

    return render(request, 'cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })


# Update cart view
@login_required
def update_cart(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        for item in cart.items.all():
            quantity_str = request.POST.get(f'quantity_{item.id}')
            if quantity_str:
                quantity = int(quantity_str)
                if quantity > 0:
                    item.quantity = quantity
                    item.save()
                else:
                    item.delete()  # Remove the item if the quantity is set to 0
        return redirect('cart_detail')
    else:
        return redirect('cart_detail')

# Remove item from cart view
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

# Checkout view (simple placeholder)
@login_required
def checkout(request):
    return render(request, 'checkout.html')


@login_required
def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code')
        cart = get_object_or_404(Cart, user=request.user)
        try:
            coupon = Coupon.objects.get(code=code)
            cart.coupon = coupon
            cart.save()
            return redirect('cart_detail')
        except Coupon.DoesNotExist:
            return redirect('cart_detail')  # Optionally, you can pass a message back
    return redirect('cart_detail')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Products.objects.filter(category=category).order_by('-id')
    return render(request, 'category_detail.html', {'category': category, 'products': products})

def products_list(request):
    products = Products.objects.all().order_by('-id')
    return render(request, 'index.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    related_products = Products.objects.filter(category=product.category).exclude(id=product.id)[:3]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
    })
