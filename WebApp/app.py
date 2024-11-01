from flask import Flask, render_template, jsonify, request
import json
import os
import uuid
from Classes.Topping import Topping
from Classes.Product import Product
from Classes.Pizza import Pizza
from Classes.Beverage import Beverage
from Classes.Order import Order

app = Flask(__name__)
app.secret_key = 'DoughminatorsKey'


def load_data():
    with open("data/toppings.json") as f:
        toppings_data = json.load(f)
    with open("data/pizzas.json") as f:
        pizzas_data = json.load(f)
    with open("data/beverages.json") as f:
        beverages_data = json.load(f)

    toppings = {topping["name"]: Topping(**topping) for topping in toppings_data}
    pizzas = []
    for pizza_data in pizzas_data:
        pizza_toppings = [toppings[name] for name in pizza_data.pop("toppings", [])]
        pizzas.append(Pizza(**pizza_data, toppings=pizza_toppings))
    beverages = [Beverage(**beverage) for beverage in beverages_data]

    return toppings, pizzas, beverages


toppings, pizzas, beverages = load_data()


def get_cart_count():
    if os.path.exists('cart.json'):
        with open('cart.json') as f:
            orders = json.load(f)
            return sum(order.get("quantity", 1) for order in orders)
    return 0


def get_total_price():
    total_price = 0
    if os.path.exists('cart.json'):
        with open('cart.json') as f:
            orders = json.load(f)
            for order in orders:
                price = order.get("price", 0)
                quantity = order.get("quantity", 1)
                total_price += price * quantity
    return total_price


def update_cart(order_data):
    item_name = order_data.get("name")
    matching_item = next((pizza for pizza in pizzas if pizza.name == item_name), None) or \
                    next((bev for bev in beverages if bev.name == item_name), None)
    if matching_item:
        order_data["id"] = str(uuid.uuid4())
        order_data["imageURL"] = matching_item.imageURL
        order_data["description"] = matching_item.description
        order_data["price"] = matching_item.price
        order_data["quantity"] = order_data.get("quantity", 1)
    if os.path.exists('cart.json'):
        with open('cart.json', 'r+') as f:
            orders = json.load(f)
            orders.append(order_data)
            f.seek(0)
            json.dump(orders, f, indent=2)
    else:
        with open('cart.json', 'w') as f:
            json.dump([order_data], f, indent=2)


@app.route("/")
def index():
    cart_count = get_cart_count()
    return render_template('home.html', cart_count=cart_count)


@app.route("/pizza")
def pizza_page():
    cart_count = get_cart_count()
    return render_template('pizza.html', pizzas=[pizza.to_dict() for pizza in pizzas], cart_count=cart_count)


@app.route("/beverages")
def beverages_page():
    cart_count = get_cart_count()
    return render_template('beverages.html', beverages=[beverage.to_dict() for beverage in beverages], cart_count=cart_count)


@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    data = request.json
    data["id"] = str(uuid.uuid4())
    update_cart(data)
    return jsonify({"status": "success", "message": "Item added to order!"})


@app.route("/cart")
def cart():
    try:
        if os.path.exists('cart.json'):
            with open('cart.json') as f:
                orders = json.load(f)
        else:
            orders = []

        enriched_orders = []
        total_price = 0
        cart_data = {}

        for order in orders:
            item_name = order.get("name")
            matching_item = next((pizza for pizza in pizzas if pizza.name == item_name), None) or \
                            next((bev for bev in beverages if bev.name == item_name), None)
            if matching_item:
                order["imageURL"] = matching_item.imageURL
                order["description"] = matching_item.description
                quantity = order.get("quantity", 1)
                item_total_price = matching_item.price * quantity
                total_price += item_total_price
                cart_data[order["id"]] = {"price": matching_item.price, "quantity": quantity}

            enriched_orders.append(order)

        cart_count = len(enriched_orders)
        return render_template('cart.html', items=enriched_orders, cart_count=cart_count, total_price=total_price, cart_data=cart_data)
    except Exception as e:
        print(f"Error loading orders: {e}")
        return jsonify({"error": "Could not load orders."}), 500


@app.route('/make_order', methods=['GET'])
def make_order():
    try:
        with open('cart.json', 'r') as file:
            items = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"error": "Cart is empty or file is missing."}), 400

    total_price = sum(item['price'] * item.get('quantity', 1) for item in items)
    
    try:
        with open('data/currentOrders.json', 'r') as file:
            current_orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        current_orders = []

    current_orders.append({"items": items, "total_price": total_price})

    with open('data/currentOrders.json', 'w') as file:
        json.dump(current_orders, file, indent=4)

    with open('cart.json', 'w') as file:
        json.dump([], file, indent=4)

    return render_template("OrderConfirmed.html", items=items, total_price=total_price)


@app.route("/getOrdersForKitchen")
def get_orders_for_kitchen():
    to_do_orders = []
    cooking_orders = []
    ready_to_serve_orders = []

    try:
        with open('data/currentOrders.json', 'r') as file:
            current_orders = json.load(file)
            for order in current_orders:
                status = order.get("status")
                if status == "TO DO":
                    to_do_orders.append(order)
                elif status == "COOKING":
                    cooking_orders.append(order)
                elif status == "READY FOR SERVING":
                    ready_to_serve_orders.append(order)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return render_template('kitchen.html',
                           to_do_orders=to_do_orders,
                           cooking_orders=cooking_orders,
                           ready_to_serve_orders=ready_to_serve_orders)


@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    data = request.json
    item_id = data.get("id")
    new_quantity = data.get("quantity")

    try:
        with open('cart.json', 'r+') as f:
            orders = json.load(f)
            for order in orders:
                if order.get("id") == item_id:
                    order["quantity"] = new_quantity
                    break
            f.seek(0)
            f.truncate()
            json.dump(orders, f, indent=2)
        
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error updating quantity: {e}")
        return jsonify({"success": False}), 500

@app.route("/pizzaInformation")
@app.route("/pizzaInformation/<pizza_name>")
def pizza_information(pizza_name):
    found_pizza = None
    for pizza in pizzas:
        if pizza.name == pizza_name:
            found_pizza = pizza
    if found_pizza:
        return render_template("pizzaInfo.html", pizza=found_pizza)
    else:
        return "Pizza not found", 400

@app.route('/remove_item', methods=['POST'])
def remove_item():
    item_id = request.json.get("id")

    try:
        with open('cart.json', 'r+') as f:
            orders = json.load(f)
            orders = [order for order in orders if order.get("id") != item_id]
            f.seek(0)
            f.truncate()
            json.dump(orders, f, indent=2)
        
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error removing item: {e}")
        return jsonify({"success": False}), 500
    

if __name__ == '__main__':
    app.run(port=8080, debug=True)
