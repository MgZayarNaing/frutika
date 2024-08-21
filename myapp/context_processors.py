# myapp/context_processors.py
from .models import Category,Cart

def category_processor(request):
    categories = Category.objects.all().order_by('-id')
    return {
        'categories': categories
    }


def cart_total(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            total_items = sum(item.quantity for item in cart.items.all())
        else:
            total_items = 0
    else:
        total_items = 0

    return {'cart_total_items': total_items}