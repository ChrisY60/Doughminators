// cart.js

let cartData = {};
let totalPrice = parseFloat(document.getElementById("totalCost").textContent) || 0;


function increaseQuantity(itemId) {
    const quantityElement = document.getElementById(`quantity-${itemId}`);
    let quantity = parseInt(quantityElement.textContent);


    quantity++;
    quantityElement.textContent = quantity;

    updateItemPrice(itemId, quantity);
    updateTotalCost();

    saveQuantityToServer(itemId, quantity);
}

function decreaseQuantity(itemId) {
    const quantityElement = document.getElementById(`quantity-${itemId}`);
    let quantity = parseInt(quantityElement.textContent);


    if (quantity > 1) {
        quantity--;
        quantityElement.textContent = quantity;

 
        updateItemPrice(itemId, quantity);
        updateTotalCost();


        saveQuantityToServer(itemId, quantity);
    }
}


function updateItemPrice(itemId, quantity) {
    const itemPriceElement = document.getElementById(`price-${itemId}`);
    const unitPrice = cartData[itemId].price; 
    const itemTotalPrice = unitPrice * quantity;


    itemPriceElement.textContent = itemTotalPrice.toFixed(2);
}


function updateTotalCost() {

    totalPrice = 0;

    Object.keys(cartData).forEach(itemId => {
        const quantity = parseInt(document.getElementById(`quantity-${itemId}`).textContent);
        const unitPrice = cartData[itemId].price;
        totalPrice += unitPrice * quantity;
    });


    document.getElementById("totalCost").textContent = totalPrice.toFixed(2);
}


function saveQuantityToServer(itemId, quantity) {
    fetch(`/update_quantity`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: itemId, quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            alert("Failed to save item quantity.");
        }
    })
    .catch(error => console.error('Error:', error));
}

function removeItem(itemId) {
    fetch(`/remove_item`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: itemId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {

            document.querySelector(`.cart-items[data-item-id="${itemId}"]`).remove();    
            delete cartData[itemId];
            updateTotalCost();
        } else {
            alert("Failed to remove item from cart.");
        }
    })
    .catch(error => console.error('Error:', error));
}

window.onload = () => {
    cartData = JSON.parse(document.getElementById("cartData").textContent);
};
