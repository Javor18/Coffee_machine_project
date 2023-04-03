function addToCart(drink_id) {
    let quantity = document.getElementById("quantity").value;
    let price = document.getElementById("price").value;
    let image = document.getElementById("image").value;

    let cart = JSON.parse(localStorage.getItem("cart"));
    if (cart == null) {
        cart = [];
    }
    cart.push({
        "drink_id": drink_id,
        "quantity": quantity,
        "price": price,
        "image": image
    });
    localStorage.setItem("cart", JSON.stringify(cart));
    alert("Drink added to cart");
}