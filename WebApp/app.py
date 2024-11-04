from flask import Flask, render_template, jsonify, request,session, redirect
import json
import os
import random
import uuid
from datetime import datetime
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


import os
import json


def update_cart(order_data):
    item_name = order_data.get("name")
    matching_item = next((pizza for pizza in pizzas if pizza.name == item_name), None) or \
                    next((bev for bev in beverages if bev.name == item_name), None)

    if matching_item:
        order_data["imageURL"] = matching_item.imageURL
        order_data["description"] = matching_item.description
        order_data["price"] = matching_item.price

        if hasattr(matching_item, 'crust'):
            order_data["crust"] = matching_item.crust
        if hasattr(matching_item, 'base'):
            order_data["base"] = matching_item.base
        if hasattr(matching_item, 'size'):
            order_data["size"] = matching_item.size
        if hasattr(matching_item, 'toppings'):
            order_data["toppings"] = [{
                "name": topping.name,
                "price": topping.price,
                "description": topping.description
            } for topping in matching_item.toppings]
        if hasattr(matching_item, 'milliliters'):
            order_data["milliliters"] = matching_item.milliliters

    if os.path.exists('cart.json'):
        with open('cart.json', 'r+') as f:
            orders = json.load(f)
            orders.append(order_data)
            f.seek(0)
            json.dump(orders, f, indent=2)
    else:
        with open('cart.json', 'w') as f:
            json.dump([order_data], f, indent=2)


toppings, pizzas, beverages = load_data()



@app.route('/')
def home():
    # Check if the table_id is in the query string
    table_id = request.args.get('table_id')
    if table_id:
        session['table_id'] = table_id  # Store the table ID in the session

    # Continue rendering the home page (or whatever you want to do)
    return render_template('home.html')  # Render your home page template

@app.route("/pizza")
def pizza_page():
    try:
        with open('cart.json', 'r') as file:
            cart = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        cart = []

    pizza_quantities = {}
    for item in cart:
        if 'name' in item:
            pizza_name = item['name']
            if pizza_name in pizza_quantities:
                pizza_quantities[pizza_name] += 1
            else:
                pizza_quantities[pizza_name] = 1

    return render_template('pizza.html', pizzas=[pizza.to_dict() for pizza in pizzas],
                            pizza_quantities=pizza_quantities)


@app.route("/beverages")
def beverages_page():
    return render_template('beverages.html', beverages=[beverage.to_dict() for beverage in beverages])


@app.route("/makeOrder", methods=['GET','POST'])
def make_order():
    # Retrieve the table ID from the session
    table_id = session.get('table_id')
    if not table_id:
        return jsonify({"error": "Table ID not found."}), 400

    try:
        with open('cart.json', 'r') as file:
            cart = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"error": "Cart is empty or file is missing."}), 400

    products = []
    for item in cart:
        if 'crust' in item and 'base' in item:
            pizza = Pizza(
                name=item['name'],
                price=item['price'],
                description=item['description'],
                imageURL=item['imageURL'],
                crust=item['crust'],
                base=item['base'],
                size=item['size'],
                toppings=[Topping(topping['name'], topping['price'], topping['description']) for topping in item.get('toppings', [])]
            )
            products.append(pizza)
        elif 'milliliters' in item:
            beverage = Beverage(
                name=item['name'],
                price=item['price'],
                description=item['description'],
                imageURL=item['imageURL'],
                milliliters=item['milliliters']
            )
            products.append(beverage)

    total_price = sum(product.price for product in products)

    # Save order with table ID
    order = Order(table_id, products, total_price)

    try:
        with open('data/currentOrders.json', 'r') as file:
            current_orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        current_orders = []

    current_orders.append(order.to_dict())

    with open('data/currentOrders.json', 'w') as file:
        json.dump(current_orders, file, indent=4)

    with open('cart.json', 'w') as file:
        json.dump([], file, indent=4)

    return render_template("OrderConfirmed.html", items=products, total_price=order.totalPrice)
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
        for order in orders:
            item_name = order.get("name")
            matching_item = next((pizza for pizza in pizzas if pizza.name == item_name), None) or \
                            next((bev for bev in beverages if bev.name == item_name), None)
            
            if matching_item:
                order["imageURL"] = matching_item.imageURL
                order["description"] = matching_item.description
            enriched_orders.append(order)

        return render_template('cart.html', items=enriched_orders)
    except Exception as e:
        print(f"Error loading orders: {e}")
        return jsonify({"error": "Could not load orders."}), 500

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
    app.run(host= '0.0.0.0',port=8080, debug=True)