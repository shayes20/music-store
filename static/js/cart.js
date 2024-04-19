function getCart() {
    let cartCookie = document.cookie.split('; ').find(row => row.startsWith('cart='));
    if (cartCookie) {
        return JSON.parse(cartCookie.split('=')[1]);
    }
    return [];
}

function updateCart(cart) {
    let cartElement = document.getElementById('cart-counter');
    let total = 0;

    for (let item of cart) {
        total += item.quantity;
    }

    if (total > 0) {
        cartElement.innerText = total;
        cartElement.classList.remove('hidden');
    } else {
        cartElement.classList.add('hidden');
    }
}

function setCart(cart) {
    document.cookie = `cart=${JSON.stringify(cart)}`;
}

function addToCart(id, name, description, image, price) {
    let cart = getCart();

    let item = cart.find(item => item.id === id);
    if (item) {
        item.quantity++;
    } else {
        cart.push({
            id: id,
            name: name,
            description: description,
            image: image,
            price: price,
            quantity: 1
        });
    }

    setCart(cart);
    updateCart(cart);
}

updateCart(getCart());