from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CoffeMachine
from django.http import JsonResponse
import json

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

def product(request, pk):
    product = CoffeMachine.objects.get(id=pk)

    # Get user informaton

    if request.method == 'POST':
        product = CoffeMachine.objects.get(id=pk)

        try:
            customer = request.user.customer

        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity = request.POST('quantity')
        orderItem.save()

        return redirect('cart')

    context = {'product': product}
    return render(request, 'product.html', context)

def cart(request):
    try:
        customer = request.user.customer

    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)


    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    context = {'order': order}
    return render(request, 'cart.html', context)
