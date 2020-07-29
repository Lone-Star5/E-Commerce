import json
from .models import *

def cookieCart(request):
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
	items = []
	order = {'getCartTotal':0, 'getCartQuantity':0,'shipping':False}
	cartItems = order['getCartQuantity']

	for i in cart:
		try:
			cartItems += cart[i]['quantity']

			product = Product.objects.get(id=i)
			total = product.price*cart[i]['quantity']

			order['getCartTotal'] += total
			order['getCartQuantity'] += cart[i]['quantity']

			item = {
				'product' : {
					'id' : product.id,
					'imageURL' : product.imageURL,
					'name' : product.name,
					'price' : product.price,
				},
				'quantity' : cart[i]['quantity'],
				'getTotal': total,
			}
			items.append(item)
			if product.digital == False:
				order['shipping'] = True
		except:
			pass

	return {'items':items, 'order':order, 'cartItems':cartItems}

def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.getCartQuantity
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']
	return {'items':items, 'order':order, 'cartItems':cartItems}

def guestOrder(request,data):
	print('Cookies: ',request.COOKIES)
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(email=email)
	customer.name = name;
	customer.save()

	order = Order.objects.create(customer=customer,complete=False)

	for item in items:
		product = Product.objects.get(id = item['product']['id'])
		orderItem = OrderItem.objects.create(
			product = product,
			order = order,
			quantity = item['quantity']
			)
	return order,customer
