// cart.js

// Initial cart data and total price based on data loaded from the server
let cartData = {}; // This will be populated with item data like prices and quantities on load
let totalPrice = parseFloat(document.getElementById("totalCost").textContent) || 0;

// Function to increase quantity
function increaseQuantity(itemId) {
    const quantityElement = document.getElementById(`quantity-${itemId}`);
    let quantity = parseInt(quantityElement.textContent);

    // Increase the quantity by 1
    quantity++;
    quantityElement.textContent = quantity;

    // Update the item's price and total cost
    updateItemPrice(itemId, quantity);
    updateTotalCost();

    // Send updated quantity to the server
    saveQuantityToServer(itemId, quantity);
}

// Function to decrease quantity
function decreaseQuantity(itemId) {
    const quantityElement = document.getElementById(`quantity-${itemId}`);
    let quantity = parseInt(quantityElement.textContent);

    // Decrease the quantity by 1 (don't go below 1)
    if (quantity > 1) {
        quantity--;
        quantityElement.textContent = quantity;

        // Update the item's price and total cost
        updateItemPrice(itemId, quantity);
        updateTotalCost();

        // Send updated quantity to the server
        saveQuantityToServer(itemId, quantity);
    }
}


function updateItemPrice(itemId, quantity) {
    const itemPriceElement = document.getElementById(`price-${itemId}`);
    const unitPrice = cartData[itemId].price; // Retrieve unit price from cartData
    const itemTotalPrice = unitPrice * quantity;

    // Update the price display for this item
    itemPriceElement.textContent = itemTotalPrice.toFixed(2);
}


// Function to update the total cost display
function updateTotalCost() {
    // Calculate the total price by summing all items in the cart
    totalPrice = 0;

    Object.keys(cartData).forEach(itemId => {
        const quantity = parseInt(document.getElementById(`quantity-${itemId}`).textContent);
        const unitPrice = cartData[itemId].price;
        totalPrice += unitPrice * quantity;
    });

    // Update the total cost display
    document.getElementById("totalCost").textContent = totalPrice.toFixed(2);
}

// Function to send updated quantity to the server
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

// Function to remove an item from the cart
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
            // Remove the item from the DOM
            document.querySelector(`.cart-items[data-item-id="${itemId}"]`).remove();

            // Update cartData and recalculate total cost
            delete cartData[itemId];
            updateTotalCost();
        } else {
            alert("Failed to remove item from cart.");
        }
    })
    .catch(error => console.error('Error:', error));
}

// Populate cartData initially with item details
window.onload = () => {
    cartData = JSON.parse(document.getElementById("cartData").textContent);
};
