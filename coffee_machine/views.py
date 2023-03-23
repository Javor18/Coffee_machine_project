from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder

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

def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = CoffeMachine.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store.html', context)

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)

def checkout(request):

    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.data)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = CoffeMachine.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


