from django.shortcuts import render
from django.http import HttpResponse
from .models import CoffeMachine
from django.http import JsonResponse

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
    # data = json.loads(request.body)
    # productId = data['productId']
    # action = data['action']
    #
    # print('Action:', action)
    # print('productId:', productId)

    return JsonResponse('Item was added', safe=False)
