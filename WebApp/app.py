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
        with open('currentOrders.json', 'r+') as f:
            orders = json.load(f)
            orders.append(order_data)
            f.seek(0)
            json.dump(orders, f, indent=2)
    else:
        with open('orders.json', 'w') as f:
            json.dump([order_data], f, indent=2)

toppings, pizzas, beverages = load_data()

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

    order = Order(4, items, sum(item.price for item in items))  # ID is auto-generated

    # Append to order history JSON
    with open("data/orderHistory.json", "a") as f:
        json.dump(order.to_dict(), f)
        f.write("\n")

    # Append to current orders JSON
    with open("data/currentOrders.json", "a") as f:
        json.dump(order.to_dict(), f)
        f.write("\n")

    return jsonify(order.to_dict())  # Return serialized order


@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    data = request.json
    save_order(data)
    return jsonify({"status": "success", "message": "Pizza added to order!"})

if __name__ == '__main__':
    app.run(port=8080)