from django.db.models import F
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, get_random_string
# from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def main(request):

    # username = get_random_string(10)
    # customer = User.objects.create_user(username, "password", f"{username}@add.com")
    # customer.save()

    if not request.COOKIES.get('order_id'):
        order = Order.objects.create(complete=False)
        order.save()
        created = True
    else:
        order = Order.objects.get(id=request.COOKIES.get('order_id'))
        created = False

    data = cartData(request)
    cartItems = data['cartItems']

    drinks = CoffeMachine.objects.all()
    items = data['items']

    context = {'drinks': drinks, 'cartItems': cartItems, 'order': order, 'items': items, 'created': created}
    response = render(request, 'main.html', context)

    if not request.COOKIES.get('order_id'):
        response.set_cookie('order_id', order.id)

    return response


def drinks(request, name):

    drink = CoffeMachine.objects.get(productName=name)
    price = drink.price_with_profit
    name = drink.productName

    if request.POST:
        order_id = request.COOKIES["order_id"]
        order_item, created = OrderItem.objects.get_or_create(order_id=order_id, product=drink)

    context = {'price': price, 'name': name, 'drink': drink}
    return render(request, 'drinks_info.html', context)



@csrf_exempt
def updateItem(request):

    data = json.loads(request.body)
    all_data = cartData(request)

    print(data)

    action = data['action']
    quantity = all_data['order']['get_cart_items']
    drink_id = int(data['product'])

    drink = CoffeMachine.objects.get(id=drink_id)

    print('Action:', action)
    print('Product:', drink)
    print('Quantity:', quantity)

    # customer = request.COOKIES.get('customer_id')
    order_id = request.COOKIES.get('order_id')


    order = Order.objects.get(id=request.COOKIES.get('order_id'))
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=drink)

    print(orderItem.id, created)
    print(orderItem.__dict__)

    if action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        if orderItem.quantity <= 0:
            orderItem.delete()

    if action == 'plus':
        orderItem.quantity = (orderItem.quantity + 1)

    if action == 'delete':
        orderItem.delete()

    cart = json.loads(request.COOKIES['cart'])
    drink_id = str(drink_id)
    cart[drink_id]['quantity'] = orderItem.quantity
    request.COOKIES['cart'] = json.dumps(cart)

    print(cart)

    orderItem.save()

    print(action, orderItem.quantity)

    return JsonResponse({"message": "ok"})


# def cart(request):
#
#     order_id = request.COOKIES.get('order_id')
#     order = Order.objects.get(id=order_id)
#     # items = Order.objects.get(id=order_id).orderitem_set.all()
#     items = cartData(request)['items']
#     cartItems = {}
#
#     for item in items:
#         cartItems[item.product.id] = {
#             'quantity': item.quantity,
#             'price': item.product.price_with_profit,
#             'name': item.product.productName,
#             'total_price': item.get_total,
#         }
#
#     data = cartData(request)
#     cartItems = data['cartItems']
#
#
#     context = {'items': items, 'order': order, 'cartItems': cartItems}
#     return render(request, 'cart.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)
