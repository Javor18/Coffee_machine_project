import json
import string
import random

from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            drink = CoffeMachine.objects.get(id=i)
            total = (drink.price_with_profit * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                'product': {
                    'id': drink.id,
                    'name': drink.productName,
                    'price': drink.price_with_profit,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):

    print(request.body)
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    drinks = CoffeMachine.objects.all()

    # product = int(request.body["product"])
    # product = request.body["product"]
    # drink = CoffeMachine.objects.get(id=product)
    cart_data = {'cartItems': cartItems, 'order': order, 'items': items, 'drinks': drinks}
    print(cart_data)
    return cart_data

# def cookieCart(request):
#     # Create empty cart for now for non-logged in user
#     try:
#         cart = json.loads(request.COOKIES['cart'])
#     except:
#         cart = {}
#         print('CART:', cart)
#
#     items = []
#     order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
#     cartItems = order['get_cart_items']
#
#     for i in cart:
#         # We use try block to prevent items in cart that may have been removed from causing error
#         try:
#             cartItems += cart[i]['quantity']
#
#             product = Product.objects.get(id=i)
#             total = (product.price * cart[i]['quantity'])
#
#             order['get_cart_total'] += total
#             order['get_cart_items'] += cart[i]['quantity']
#
#             item = {
#                 'id': product.id,
#                 'product': {'id': product.id, 'name': product.name, 'price': product.price,
#                             'quantity': cart[i]['quantity'],
#                 'digital': product.digital, 'get_total': total,
#             }
#             }
#             items.append(item)
#
#             if product.digital == False:
#                 order['shipping'] = True
#         except:
#             pass
#
#     return {'cartItems': cartItems, 'order': order, 'items': items}

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)

    return result_str