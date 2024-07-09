# views.py
from django.shortcuts import render

from .cart import Cart
from store.models import Category, Product, Size
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart': cart})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        product_size = request.POST.get('product_size')
        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, name=product_size)
        cart.add(product=product, product_qty=product_quantity, product_size=size)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_size = request.POST.get('product_size')
        cart.delete(product_id=product_id, size_name=product_size)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total()
        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        product_size = request.POST.get('product_size')
        cart.update(product_id=product_id, qty=product_quantity, size_name=product_size)
        cart_quantity = cart.__len__()
        cart_total = cart.get_total()
        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})
        return response
