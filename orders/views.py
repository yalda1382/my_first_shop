from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem

def cart_view(request):
    cart = request.session.get('cart', {})  # { "product_id": qty, ... }
    products = Product.objects.filter(id__in=[int(i) for i in cart.keys()]) if cart else []
    cart_items = []
    total = 0
    for p in products:
        qty = cart.get(str(p.id), 0)
        item_total = p.price * qty
        cart_items.append({'product': p, 'quantity': qty, 'total': item_total})
        total += item_total

    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total_price': total})

def add_to_cart(request, product_id):
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + qty
        request.session['cart'] = cart
    return redirect('/orders/cart/')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('/orders/cart/')

def delete_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('/orders/cart/')

def checkout(request):
    cart = request.session.get('cart', {})
    if cart:
        products = Product.objects.filter(id__in=[int(i) for i in cart.keys()])
        order = Order.objects.create(user=request.user)
        for p in products:
            OrderItem.objects.create(order=order, product=p, quantity=cart[str(p.id)])
        order.ordered = True
        order.save()
    return redirect('cart_view')

@login_required(login_url='login')
def orders_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/orders_list.html', {'orders': orders})