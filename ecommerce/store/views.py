from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *

# Create your views here.

def index(request):
	return render(request,'store/main.html')

def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.getCartQuantity
	else:
		items = []
		order = {'getCartTotal':0, 'getCartQuantity':0, 'shipping':False}
		cartItems = order['getCartQuantity']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request,'store/store.html',context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.getCartQuantity
	else:
		items = []
		order = {'getCartTotal':0, 'getCartQuantity':0,'shipping':False}
		cartItems = order['getCartQuantity']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request,'store/cart.html',context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.getCartQuantity
	else:
		items = []
		order = {'getCartTotal':0, 'getCartQuantity':0,'shipping':False}
		cartItems = order['getCartQuantity']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request,'store/checkout.html',context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id = productId)
	order,created = Order.objects.get_or_create(customer=customer,complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) 

	if action == 'add':
		orderItem.quantity = orderItem.quantity + 1
	elif action == 'remove':
		orderItem.quantity = orderItem.quantity -1

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer,complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id
		if order.getCartTotal == total:
			order.complete=True
		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
					customer = customer,
					order = order,
					address = data['shipping']['address'],
					city = data['shipping']['city'],
					state = data['shipping']['state'],
					zipcode = data['shipping']['zipcode'],

				)

	else:
		print('User not logged in')

	return JsonResponse('payment successfull',safe = False)