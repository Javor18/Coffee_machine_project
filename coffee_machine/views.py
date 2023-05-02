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
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    data = cartData(request)
    print(data)

    # if request.user.is_authenticated:

    # customer = request.user.customer

    # order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order = data['order']

    # created = data['created']
    # items = order.orderitem_set.all()

    items = data['items']

    # cartItems = order.get_cart_items

    cartItems = data['cartItems']

    # else:
    #
    #     # Create empty cart for now for non-logged in user
    #
    #     items = []
    #     order = {'get_cart_total': 0, 'get_cart_items': 0}
    #     cartItems = order['get_cart_items']

    drinks = CoffeMachine.objects.all()
    context = {'drinks': drinks, 'cartItems': cartItems, 'customer': customer.id, 'order': order, 'items': items, 'created': created}
    response = render(request, 'main.html', context)
    response.set_cookie('customer_id', customer.id)
    response.set_cookie('order_id', order)


    return response


def drinks(request, name):

    data = cartData(request)

    # if request.user.is_authenticated:

    # customer = request.user.customer
    # order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order = data['order']

    # items = order.orderitem_set.all()

    items = data['items']

    # cartItems = order.get_cart_items

    cartItems = data['cartItems']

    # else:
    #
    #     # Create empty cart for now for non-logged in user
    #
    #     items = []
    #     order = {'get_cart_total': 0, 'get_cart_items': 0}
    #     cartItems = order['get_cart_items']

    # drink = CoffeMachine.objects.get(productName=name)
    drink = CoffeMachine.objects.get(productName=name)
    price = drink.price_with_profit
    name = drink.productName
    context = {'price': price, 'name': name, 'drink': drink}
    return render(request, 'drinks_info.html', context)



@csrf_exempt
def updateItem(request):

    data = json.loads(request.body)
    all_data = cartData(request)

    print(data)
    # print(all_data)

    action = data['action']
    quantity = all_data['order']['get_cart_items']
    drink_id = int(data['product'])

    drink = CoffeMachine.objects.get(id=drink_id)

    print('Action:', action)
    print('Product:', drink)
    print('Quantity:', quantity)

    customer = request.COOKIES.get('customer_id')

    order, created = Order.objects.get(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get(order=order, product_id=drink_id)
    print(orderItem.__dict__)

    print(orderItem.quantity)

    if action == 'remove':
        # orderItem.quantity = (orderItem.quantity - 1)
        orderItem.quantity -= 1

    if action == 'plus':
        # orderItem.quantity = (orderItem.quantity + 1)
        orderItem.quantity += 1

    if action == 'delete':
        orderItem.delete()

    orderItem.save()
    print(action, orderItem.quantity)

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({"message": "ok"})


def cart(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
            # Order.objects.get(id=customer_id)
        except:
            cart = {}
        print('Cart:', cart)
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
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

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)

