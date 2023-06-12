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

    username = get_random_string(10)
    customer = User.objects.create_user(username, "password", f"{username}@add.com")
    customer.save()

    if not request.COOKIES.get('order_id'):
        order = Order.objects.create(customer=customer, complete=False)
        order.save()
        created = True
    else:
        order = Order.objects.get(id=request.COOKIES.get('order_id'))
        created = False

    data = cartData(request)
    cartItems = data['cartItems']

    drinks = CoffeMachine.objects.all()
    items = data['items']

    context = {'drinks': drinks, 'cartItems': cartItems, 'customer': customer.id, 'order': order, 'items': items, 'created': created}
    response = render(request, 'main.html', context)

    if not request.COOKIES.get('order_id'):
        # response.set_cookie('customer_id', customer.id)
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
    # all_data = cartData(request)

    print(data)
    # print(all_data)

    action = data['action']
    # quantity = all_data['order']['get_cart_items']
    quantity = data['quantity']
    drink_id = int(data['productId'])
    print("Drink id -----------")
    print(drink_id)

    drink = CoffeMachine.objects.get(id=drink_id)

    print('Action:', action)
    print('Product:', drink)
    print('Quantity:', quantity)

    customer = request.COOKIES.get('customer_id')
    order_id = request.COOKIES.get('order_id')

    order = Order.objects.get(id=request.COOKIES.get('order_id'))
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=drink)

    print(action)

    print(orderItem.id, created)

    orderItem.quantity += int(quantity)

    if action == 'remove':
        if orderItem.quantity <= 0:
            orderItem.delete()

    if action == 'delete':
        orderItem.delete()

    # cart = json.loads(request.COOKIES['cart'])
    # drink_id = str(drink_id)
    # cart[drink_id]['quantity'] = orderItem.quantity


    orderItem.save()

    print(action, orderItem.quantity)

    return JsonResponse({"message": "ok"})


def cart(request):

    # if request.user.is_authenticated:
    #     customer = request.user
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order['get_cart_items']

    order_id = request.COOKIES.get('order_id')
    order = Order.objects.get(id=order_id)
    items = Order.objects.get(id=order_id).orderitem_set.all()

    cartItems = {}

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)

