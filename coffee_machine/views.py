from django.db.models import F
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, get_random_string


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

    drinks = CoffeMachine.objects.all()

    context = {'drinks': drinks, 'customer': customer.id, 'order': order, 'created': created}
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

    print("update item calls")

    data = json.loads(request.body)
    print(data)

    action = data['action']
    quantity = data['quantity']
    drink_id = int(data['productId'])
    print("Drink id -----------")
    print(drink_id)
    total_price = 0

    drink = CoffeMachine.objects.get(id=drink_id)

    print('Action:', action)
    print('Product:', drink)
    print('Quantity:', quantity)

    order = Order.objects.get(id=request.COOKIES.get('order_id'))
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=drink)

    print(action)

    print(orderItem.id, created)

    if quantity != None:
        orderItem.quantity = int(quantity)

    if action == 'remove':
        if orderItem.quantity <= 0:
            orderItem.delete()

    if action == 'delete':
        orderItem.delete()

        print("delete item")

    else:
        orderItem.save()

    print(action, orderItem.quantity)

    return JsonResponse({"message": "ok"})


def cart(request):


    order_id = request.COOKIES.get('order_id')
    order = Order.objects.get(id=order_id)
    items = Order.objects.get(id=order_id).orderitem_set.all()
    total_items = 0
    total_price = 0

    print(items)
    print(order)

    for item in order.orderitem_set.all():
        print(item.product.productName, item.quantity)
        total_price += item.get_total
        total_items += item.quantity

    print(total_price, total_items)

    context = {'items': items, 'order': order, 'total_items': total_items, 'total_price': total_price}
    return render(request, 'cart.html', context)

