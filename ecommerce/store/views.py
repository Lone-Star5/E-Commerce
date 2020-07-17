from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
	return render(request,'store/main.html')

def store(request):
	products = Product.objects.all()
	return render(request,'store/store.html',{'products':products})

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'getCartTotal':0, 'getCartQuantity':0}
	context = {'items':items, 'order':order}
	return render(request,'store/cart.html',context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'getCartTotal':0, 'getCartQuantity':0}
	context = {'items':items, 'order':order}
	return render(request,'store/checkout.html',context)