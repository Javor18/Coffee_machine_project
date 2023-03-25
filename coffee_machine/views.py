from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
import datetime

from .models import *
# from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def main(request):
    drinks = CoffeMachine.objects.all()
    return render(request, 'main.html', {"drinks": drinks})


def drinks(request, name):
    drink = CoffeMachine.objects.get(productName=name)
    price = drink.price_with_profit
    name = drink.productName
    context = {'price': price, 'name': name, 'drink': drink}
    return render(request, 'drinks_info.html', context)


# ///////////// Add to cart //////////////////


# def product(request, pk):
#     product = CoffeMachine.objects.get(id=pk)
#
#     # Get user informaton
#
#     if request.method == 'POST':
#         product = CoffeMachine.objects.get(id=pk)
#
#         try:
#             customer = request.user.customer
#
#         except:
#             device = request.COOKIES['device']
#             customer, created = Customer.objects.get_or_create(device=device)
#
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
#         orderItem.quantity = request.POST('quantity')
#         orderItem.save()
#
#         return redirect('cart')
#
#     context = {'product': product}
#     return render(request, 'product.html', context)





# def store(request):
#
#     data = cartData(request)
#     cartItems = data['cartItems']
#
#     products = CoffeMachine.objects.all()
#     context = {'products': products, 'cartItems': cartItems}
#     return render(request, 'store.html', context)
#
# def cart(request):
#
#     data = cartData(request)
#     cartItems = data['cartItems']
#     order = data['order']
#     items = data['items']
#
#     context = {'items': items, 'order': order, 'cartItems': cartItems}
#     return render(request, 'cart.html', context)
#
# def checkout(request):
#
#     data = cookieCart(request)
#     cartItems = data['cartItems']
#     order = data['order']
#     items = data['items']
#
#     context = {'items': items, 'order': order, 'cartItems': cartItems}
#     return render(request, 'checkout.html', context)
#
# def updateItem(request):
#     data = json.loads(request.data)
#     productId = data['productId']
#     action = data['action']
#
#     print('Action:', action)
#     print('productId:', productId)
#
#     customer = request.user.customer
#     product = CoffeMachine.objects.get(id=productId)
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#
#     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
#
#     if action == 'add':
#         orderItem.quantity = (orderItem.quantity + 1)
#     elif action == 'remove':
#         orderItem.quantity = (orderItem.quantity - 1)
#
#     orderItem.save()
#
#     if orderItem.quantity <= 0:
#         orderItem.delete()
#
#     return JsonResponse('Item was added', safe=False)


# /////////////  View for adding items to the cart  //////////////

def add_to_cart(request, drink_id):

    drink = CoffeMachine.objects.get(id=drink_id)
    cart = request.session.get('cart', {})
    cart[drink_id] = {
        'name': drink_id.productName,
        'price': drink_id.price_with_profit,
        'quantity': cart.get(drink_id, {}).get('quantity', 0) + 1
    }

    request.session['cart'] = cart
    return redirect('cart')


# /////////////  View for displaying items in the cart  //////////////
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for drink_id, drink_data in cart.items():
        drink_price = float(drink_data['price']) * drink_data['quantity']

        cart_items.append({
            'id': drink_id,
            'name': drink_data['name'],
            'price': drink_data['price'],
            'quantity': drink_data['quantity'],
            'drink_price': drink_price,
        })
        total_price += drink_price
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

# /////////////  View for removing items from the cart  //////////////
def remove_from_cart(request, drink_id):
    cart = request.session.get('cart', {})

    if drink_id in cart:
        del cart[drink_id]
        request.session['cart'] = cart
    return redirect('cart')