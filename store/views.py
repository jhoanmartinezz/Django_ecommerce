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
    # Information Of What User Has Done
    data = json.loads(request.body.decode('utf-8'))
    #json.loads(request.body)
    # Product To Buy ID
    productID = data['productId']
    # Action To Add To Cart Or Something Else You Do
    action = data['action']
    # Print To Make Sure It Workds
    print('Action:',action)
    # Print To Make Sure It Workds
    print('productID:', productID)
    # Show The Data Above Is Chrome Console As Well
    return JsonResponse('item was added',safe=False)
