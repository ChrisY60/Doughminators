
const orderModal = document.getElementById("orderModal");
const orderButton = document.querySelector(".order-now-btn");
const backButton = document.getElementById("backButton");
const confirmButton = document.getElementById("confirmButton");


orderButton.onclick = function() {
    orderModal.style.display = "block";
};


backButton.onclick = function() {
    orderModal.style.display = "none";
};


confirmButton.onclick = function() {
    orderModal.style.display = "none";

    window.location.href = makeOrderUrl; 
};

window.onclick = function(event) {
    if (event.target === orderModal) {
        orderModal.style.display = "none";
    }
};
