from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cartData, guestOrder
from .decorators import unauthenticated_user
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateCustomerForm

def homepage(request):
	data = cartData(request)
	items = data['items']
	order = data['order']
	cartItems = data['cartItems']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/homepage.html', context)

def store(request):
	data = cartData(request)
	items = data['items']
	order = data['order']
	cartItems = data['cartItems']

	products = Product.objects.all()
	context = {'products':products, 'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):
	data = cartData(request)
	items = data['items']
	order = data['order']
	cartItems = data['cartItems']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	items = data['items']
	order = data['order']
	cartItems = data['cartItems']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	
	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id = productId)
	order, created = Order.objects.get_or_create(customer = customer, complete = False)
	orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

	if action == 'remove':
		orderItem.delete()

	return JsonResponse("Item was added", safe = False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete = False)

	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	ShippingAddress.objects.create(
	customer = customer,
	order = order,
	address = data['shipping']['address'],
	city = data['shipping']['city'],
	state = data['shipping']['state'],
	zipcode = data['shipping']['zipcode'],
	)

	return JsonResponse('Payment submitted..', safe = False)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, 'Username OR Password is incorrect!')
            return render(request, 'store/login.html')

    context = {}

    return render(request, 'store/login.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'Successfully logged out!')
    return redirect('login')

@unauthenticated_user
def registerPage(request):
	form = CreateCustomerForm
    
	if request.method == 'POST':
		form = CreateCustomerForm(request.POST)
		if form.is_valid():
			form.save()
			uname = form.cleaned_data.get('username')
			user = User.objects.get(username = uname)
			name = form.cleaned_data.get('first_name')
			email = form.cleaned_data.get('email')
			customer, created = Customer.objects.get_or_create(user = user, name = name, email = email)
			customer.save()
			messages.success(request, name + ' was registered successfully!')
			return redirect('login')

	context = {'form':form}

	return render(request, 'store/register.html', context)

def myOrders(request):
	orders = Order.objects.filter(customer = request.user.id).order_by('-date_ordered')

	context = {'orders':orders}

	return render(request, 'store/myorders.html', context)