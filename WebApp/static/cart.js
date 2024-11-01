// cart.js

function removeItem(itemId) {
    fetch(`/remove_item`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: itemId }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Refresh the page to update the cart view
            window.location.reload();
        } else {
            alert("Failed to remove item from cart.");
        }
    })
    .catch(error => console.error('Error:', error));
}
