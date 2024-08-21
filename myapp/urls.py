from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/', views.products_list, name='products_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
