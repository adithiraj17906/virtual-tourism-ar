from django.db import models
from django.utils import timezone  

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    VRimage = models.ImageField(upload_to='vr_images/', null=True, blank=True)  
    location = models.CharField(max_length=100)
    season = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField(blank=True, null=True) 

    def __str__(self):
        return self.title

class ARProduct(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='ar_products/')
    ar_link = models.URLField(blank=True, null=True)
    review = models.TextField(blank=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery/')
    alt_text = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.title}"

from django.db import models
from shop.models import Product, ARProduct  # adjust import as needed

class CartItem(models.Model):
    session_id = models.CharField(max_length=255)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    ar_product = models.ForeignKey(ARProduct, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_selected = models.DateField(null=True, blank=True)
    time_slot = models.CharField(max_length=100, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title if self.product else self.ar_product.title

from django.db import models
from .models import Product, ARProduct

class Order(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()  
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    ar_product = models.ForeignKey(ARProduct, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
