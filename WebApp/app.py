from flask import Flask, render_template, jsonify, request
import json
import os
import random
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


def save_order(order_data):
    if os.path.exists('orders.json'):
        with open('orders.json', 'r+') as f:
            orders = json.load(f)
            orders.append(order_data)
            f.seek(0)
            json.dump(orders, f, indent=2)
    else:
        with open('orders.json', 'w') as f:
            json.dump([order_data], f, indent=2)

# Load the data once at the start
toppings, pizzas, beverages = load_data()


def add_order_to_current_orders(order):
    with open('data/currentOrders.json', 'r+') as f:
        print("a")

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/pizza")
def pizza_page():
    return render_template('pizza.html', pizzas=[pizza.to_dict() for pizza in pizzas])

@app.route("/beverages")
def beverages_page():
    return render_template('beverages.html', beverages=[beverage.to_dict() for beverage in beverages])

@app.route("/makeOrder")
def make_order():
    selected_pizza = random.choice(pizzas)
    selected_beverage = random.choice(beverages)
    items = [selected_pizza, selected_beverage]

    order = Order(4, items, sum(item.price for item in items))

    try:
        with open('data/currentOrders.json', 'r') as file:
            current_orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        current_orders = []

    current_orders.append(order.to_dict())

    with open('data/currentOrders.json', 'w') as file:
        json.dump(current_orders, file, indent=4)

    return jsonify(order.to_dict())


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
    save_order(data)
    return jsonify({"status": "success", "message": "Item added to order!"})

@app.route("/cart")
def cart():
    try:
        # Your code to read from orders.json
        if os.path.exists('orders.json'):
            with open('orders.json') as f:
                orders = json.load(f)
        else:
            orders = []

        return render_template('cart.html', items=orders)
    except Exception as e:
        print(f"Error loading orders: {e}")
        return jsonify({"error": "Could not load orders."}), 500
if __name__ == '__main__':
    app.run(port=8080, debug=True)
