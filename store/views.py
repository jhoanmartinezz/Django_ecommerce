from django.shortcuts import render

# Create your views here.
from .models import *
from django.http import JsonResponse
import json

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,"store/store.html", context)

def cart(request):
    if request.user.is_authenticated:
        client = request.user.customer
        order, created = Order.objects.get_or_create(customer=client, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0}
    context = {'items':items,'order':order}
    return render(request,"store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        client = request.user.customer
        order, created = Order.objects.get_or_create(customer=client, complete=False)
        items = order.orderitem_set.all()
    else:
        order = {'get_cart_total':0,'get_cart_items':0}
        items = []
    context = {'items':items,'order':order}
    return render(request,"store/checkout.html",context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productid']
    action = data['action']
    print('Action:',action)
    print('productID:', productID)
    return JsonResponse('item was added',safe=False)
