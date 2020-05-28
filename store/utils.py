import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart view py:', cart)
    items = []
    order = {'get_cart_total':0,'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']
    #actualizar los items y el total dentro del for
    for k in cart:
        #try para producto inexistente en la base de datos
        try:
            cartItems += cart[k]["quantity"]
            product = Product.objects.get(id=k)
            total = (product.price * cart[k]["quantity"])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[k]["quantity"]
            item = {
                    'product':{
                                'id':product.id,
                                'name':product.name,
                                'price':product.price,
                                'imageURL':product.imageURL,
                               },
                    'quantity':cart[k]["quantity"],
                    'get_cart_total':total
                    }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems,'order':order,'items':items}
