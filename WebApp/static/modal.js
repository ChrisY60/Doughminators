// Get modal and buttons
const orderModal = document.getElementById("orderModal");
const orderButton = document.querySelector(".order-now-btn");
const backButton = document.getElementById("backButton");
const confirmButton = document.getElementById("confirmButton");

// Show modal when "Order Now" is clicked
orderButton.onclick = function() {
    orderModal.style.display = "block";
};

// Hide modal when "Back" is clicked
backButton.onclick = function() {
    orderModal.style.display = "none";
};

// Confirm action when "Confirm" is clicked
confirmButton.onclick = function() {
    orderModal.style.display = "none";
    // Redirect to make order or submit the form
    window.location.href = makeOrderUrl; // Assuming makeOrderUrl is defined
};

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
    if (event.target === orderModal) {
        orderModal.style.display = "none";
    }
};
