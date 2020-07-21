let updateBtns = document.getElementsByClassName('update-cart');

Array.prototype.forEach.call(updateBtns,item => {
	item.addEventListener('click',()=>{
		let productId = item.dataset.product;
		let action = item.dataset.action;

		if(user==='AnonymousUser'){
			console.log('no access');
		}
		else{
			updateUserOrder(productId,action);
		}
	})
});

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