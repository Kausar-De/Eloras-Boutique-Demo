var updateBtns = document.getElementsByClassName("update-cart")

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener("click", function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log("productId:", productId, "Action:", action)
		console.log("USER:", user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}
		else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log("User is authenticated, sending data...")

		var url = "/update_item/"

		fetch(url, {
			method:"POST",
			headers:{
				"Content-Type":"application/json",
				"X-CSRFToken":csrftoken,
			}, 
			body:JSON.stringify({"productId": productId, "action": action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    console.log("data:", data)
			location.reload()
		});
}

function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
          } 
        }
        return cookieValue;
}

const csrftoken = getToken('csrftoken');

function getCookie(name) {
	// Split cookie string and get all individual name=value pairs in an array
	var cookieArr = document.cookie.split(";");

	// Loop through the array elements
	for(var i = 0; i < cookieArr.length; i++) {
		var cookiePair = cookieArr[i].split("=");

		/* Removing whitespace at the beginning of the cookie name
		and compare it with the given string */
		if(name == cookiePair[0].trim()) {
			// Decode the cookie value and return
			return decodeURIComponent(cookiePair[1]);
		}
	}

	// Return null if not found
	return null;
}
var cart = JSON.parse(getCookie('cart'))

if (cart == undefined){
	cart = {}
	console.log('Cart Created!', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
}
console.log('Cart:', cart)


function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = productId;
		}
	}

	if (action == 'remove'){
		console.log('Item should be deleted')
		delete cart[productId];
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}