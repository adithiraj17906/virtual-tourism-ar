from django.contrib import admin
from .models import Product, ProductImage, ARProduct, OrderItem, Order

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['title', 'price', 'location']
    list_filter = ['location', 'season']
    search_fields = ['title', 'description']
    
    fields = ['title', 'description', 'price', 'image', 'VRimage', 'location', 'season', 'video_url']

admin.site.register(Product, ProductAdmin)
admin.site.register(ARProduct)
admin.site.register(OrderItem)  
admin.site.register(Order)
