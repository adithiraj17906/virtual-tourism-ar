from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, CartItem, ARProduct
import qrcode
import base64
from io import BytesIO
from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def ar_shop(request):
    products = ARProduct.objects.all()
    return render(request, 'shop/ar_shop.html', {'products': products})

def ar_product_detail(request, pk):
    product = get_object_or_404(ARProduct, pk=pk)
    qr_code_base64 = generate_qr_code(product.ar_link)

    return render(request, 'shop/ar_product_detail.html', {
        'product': product,
        'qr_code_base64': qr_code_base64
    })

def generate_qr_code(url):
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return qr_image_base64



def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')


def add_to_cart(request, product_id):
    if request.method == 'POST':
        # Check if this is an AR product or regular product
        product_type = request.POST.get('product_type', 'regular')
        
        if product_type == 'ar':
            # This is an AR product
            ar_product = get_object_or_404(ARProduct, id=product_id)
            selected_product = None
            is_ar = True
            product_name = ar_product.title
            product_price = ar_product.price
        else:
            # This is a regular product
            selected_product = get_object_or_404(Product, id=product_id)
            ar_product = None
            is_ar = False
            product_name = selected_product.name
            product_price = selected_product.price

        date = request.POST.get('date_selected') or request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        quantity = int(request.POST.get('quantity', 1))

        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key

        cart_item, created = CartItem.objects.get_or_create(
            session_id=session_id,
            date_selected=date,
            time_slot=time_slot,
            product=selected_product,
            ar_product=ar_product,
            defaults={
                'quantity': quantity,
                'total_price': product_price * quantity
            }
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.total_price = product_price * cart_item.quantity
            cart_item.save()

        messages.success(
            request,
            f"{product_name} added to cart successfully!"
        )
        return redirect('cart')

    # GET request - redirect back to product detail
    try:
        Product.objects.get(id=product_id)
        return redirect('product_detail', pk=product_id)
    except Product.DoesNotExist:
        return redirect('ar_product_detail', pk=product_id)


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')


def cart_view(request):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    cart_items = CartItem.objects.filter(session_id=session_id).order_by('-created_at')
    cart_total = sum(item.total_price for item in cart_items)

    tax_rate = Decimal('0.18')
    tax_amount = (cart_total * tax_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    final_total = (cart_total + tax_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tax_amount': tax_amount,
        'final_total': final_total,
    }
    return render(request, 'shop/cart.html', context)

def add_to_cart_ar(request, product_id):
    product = get_object_or_404(ARProduct, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))
    date = request.POST.get('date')
    time_slot = request.POST.get('time_slot')

   
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    CartItem.objects.create(
        ar_product=product,
        quantity=quantity,
        date_selected=date,
        time_slot=time_slot,
        session_id=session_key,
        total_price=product.price * quantity
    )

    messages.success(request, "AR Experience added to cart!")
    return redirect('cart')

from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect(reverse('product_list') + '?registered=true') 
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

from django.shortcuts import render, redirect
from .models import CartItem

from django.shortcuts import render, redirect
from .models import CartItem, Order
from .forms import OrderForm  
from django.contrib.auth.decorators import login_required



from django.shortcuts import redirect

@login_required

def checkout_view(request):
    if request.method == 'POST':

        session_id = request.session.session_key
        CartItem.objects.filter(session_id=session_id).delete()

        return redirect('checkout_success') 

    cart_items = CartItem.objects.filter(session_id=request.session.session_key)
    total = sum(item.total_price for item in cart_items)
    form = OrderForm()

    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form,
    }
    return render(request, 'shop/checkout.html', context)

def checkout_success(request):
    return render(request, 'shop/checkout_success.html')

