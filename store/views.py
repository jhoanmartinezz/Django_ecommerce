from django.shortcuts import render

# Create your views here.
from .models import *

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,"store/store.html", context)

def cart(request):
    context = {}
    return render(request,"store/cart.html", context)

def checkout(request):
    context = {}
    return render(request,"store/checkout.html",context)
