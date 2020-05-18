from django.shortcuts import render

# Create your views here.
from .models import *
from django.http import JsonResponse
import json
import datetime

def store(request):
    if request.user.is_authenticated:
        client = request.user.customer
        order, created = Order.objects.get_or_create(customer=client, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0,'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems,}
    return render(request,"store/store.html", context)

def cart(request):
    if request.user.is_authenticated:
        client = request.user.customer
        order, created = Order.objects.get_or_create(customer=client, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,"store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        client = request.user.customer
        order, created = Order.objects.get_or_create(customer=client, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0,'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        items = []
    context = {'items':items,'order':order,'cartItems':cartItems}
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
    customer = request.user.customer
    product = Product.objects.get(id=productID)
    #create the order
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    #add or delete
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    # Show The Data Above Is Chrome Console As Well
    return JsonResponse('item was added',safe=False)

def processOrder(request):
    #print("Data",request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body.decode('utf-8'))
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
	#else:
    #customer, order = guestOrder(request, data)
    #total = float(data['form']['total'])
    #order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
        	order=order,
        	address=data['shipping']['address'],
        	city=data['shipping']['city'],
        	state=data['shipping']['state'],
        	zipcode=data['shipping']['zipcode'],
        	)
    else:
        print("Usert not logged in...")
    return JsonResponse('Payment submitted..', safe=False)
