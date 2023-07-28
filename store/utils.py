import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
    
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = len(cart)

    for i in cart.values():
        try:
            product = Product.objects.get(id = i)
            total  = product.price

            order['get_cart_total'] += total
            order['get_cart_items'] = len(cart)

            item = {
                'id': product.id,
                'product':{
                    'id': product.id,
                    'name': product.name, 
                    'price': product.price,
                    'category': product.category,
                    'colour': product.colour,
                    'size': product.size,
                    'fabric': product.fabric,
                    'imageURL':product.imageURL,
                    }, 
                'get_total': total,
                }
            items.append(item)
        except:
            pass

    return {'items':items, 'order':order, 'cartItems':cartItems}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
                
    return {'items':items, 'order':order, 'cartItems':cartItems}

def guestOrder(request, data):
    print('User is not logged in')

    print('COOKIES: ', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email = email,)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer = customer, complete = False,)

    for item in items:
        product = Product.objects.get(id = item['id'])
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
        )

    return customer, order