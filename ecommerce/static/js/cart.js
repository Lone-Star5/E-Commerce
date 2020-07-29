let updateBtns = document.getElementsByClassName('update-cart');

Array.prototype.forEach.call(updateBtns,item => {
	item.addEventListener('click',()=>{
		let productId = item.dataset.product;
		let action = item.dataset.action;

		if(user==='AnonymousUser'){
			addCookieItem(productId,action);
		}
		else{
			updateUserOrder(productId,action);
		}
	})
});

addCookieItem = (productId, action) => {
	if(action=='add'){
		if(cart[productId]==undefined){
			cart[productId] = {'quantity':1}
		}
		else{
			cart[productId]['quantity'] += 1;
		}
	}
	if(action == 'remove'){
		cart[productId]['quantity'] -= 1;
		if(cart[productId]['quantity']<=0){
			delete cart[productId];
		}
	}
	console.log("cart: ",cart);
	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
	location.reload();
}

updateUserOrder = (productId, action) => {
	console.log('access')

	let url = '/update/';

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({'productId':productId, 'action': action})
	})

	.then( response => response.json())

	.then((data) => {
		console.log('data: ',data);
		location.reload();
	})
}