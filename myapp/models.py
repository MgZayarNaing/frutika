from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Products(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    normal_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2 , null=True, blank=True)
    weight = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart ({self.user.username})"

    def total_price(self):
        total = sum(item.total_price() for item in self.items.all())
        if self.coupon:
            discount = min(self.coupon.discount, total)  # Ensure discount doesn't exceed total
            total -= discount
        return total



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        if self.product.sale_price:
            return self.product.sale_price * self.quantity
        return self.product.normal_price * self.quantity

