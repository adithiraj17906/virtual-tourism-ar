from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #  Root URL — Login page
    path('login/', auth_views.LoginView.as_view(
        template_name='shop/login.html',
        redirect_authenticated_user=True,
        next_page='checkout'
    ), name='login'),

    #  Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    #  Registration
    path('register/', views.register, name='register'),

    #  Main page after login
    path('', views.product_list, name='product_list'),


    #  Product & AR Product views
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('ar-shop/', views.ar_shop, name='ar_shop'),
    path('ar-product/<int:pk>/', views.ar_product_detail, name='ar_product_detail'),
    
    #  Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    #  Cart functionality
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-cart-ar/<int:product_id>/', views.add_to_cart_ar, name='add_to_cart_ar'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),


    path('checkout/', views.checkout_view, name='checkout'),

    path('checkout/success/', views.checkout_success, name='checkout_success'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)