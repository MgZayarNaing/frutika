from django.contrib import admin
from .models import Category, Products, Coupon, Cart, CartItem

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'normal_price', 'sale_price', 'weight', 'created_at']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'created_at']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount']
    search_fields = ['code']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon', 'created_at', 'updated_at']
    search_fields = ['user__username']
    list_filter = ['created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['cart__user__username', 'product__name']
    list_filter = ['cart__created_at']
