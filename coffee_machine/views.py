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


# /////////////  View for adding items to the cart  //////////////

def add_to_cart(request, drink_id):

    # drink = CoffeMachine.objects.get(id=drink_id)
    # cart = request.session.get('cart', {})
    # cart[drink_id] = {
    #     'name': drink_id.productName,
    #     'price': drink_id.price_with_profit,
    #     'quantity': cart.get(drink_id, {}).get('quantity', 0) + 1
    # }
    #
    # request.session['cart'] = cart
    # return redirect('cart')

    if request.method == 'POST':
        user = request.user
        drink_name = request.POST.get('drink_name')
        drink_price = request.POST.get('drink_price')
        quantity = request.POST.get('quantity')
        cart_item = Cart(user=user, drink_name=drink_name, drink_price=drink_price, quantity=quantity)
        cart_item.save()

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

# /////////////  View for cart  //////////////

def cart(request):

    cart_item = Cart.objects.filter(user=request.user)
    context = {'cart_item': cart_item}
    return render(request, 'cart.html', context)
