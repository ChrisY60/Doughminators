function addToOrder(name, price) {
    const orderData = {
        name: name,
        price: price
    };

    fetch('/add_to_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Handle success message
        alert(data.message); // Notify user of success
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
