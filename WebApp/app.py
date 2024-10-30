from flask import Flask, render_template, jsonify
from datetime import datetime

from Classes.Topping import *
from Classes.Product import *
from Classes.Pizza import *
from Classes.Beverage import *
from Classes.Order import *

app = Flask(__name__)
app.secret_key = 'DoughminatorsKey'


topping_cheese = Topping("Extra Cheese", 1.00, "Mozzarella cheese")
topping_olives = Topping("Olives", 0.75, "Green olives")
topping_mushrooms = Topping("Mushrooms", 0.80, "Fresh mushrooms")
topping_pepperoni = Topping("Pepperoni", 1.50, "Spicy pepperoni slices")
topping_bell_peppers = Topping("Bell Peppers", 0.70, "Colorful bell peppers")


pizzas = [
    Pizza("Margherita", 8.00, "Classic cheese and tomato pizza", "image_url", "thin", "tomato", "medium", [topping_cheese]),
    Pizza("Pepperoni", 9.50, "Pepperoni with mozzarella cheese", "image_url", "thick", "tomato", "large", [topping_pepperoni, topping_cheese]),
    Pizza("Veggie", 9.00, "Bell peppers, olives, onions, and tomatoes", "image_url", "thin", "tomato", "medium", [topping_olives, topping_bell_peppers, topping_mushrooms])
]


beverages = [
    Beverage("Cola-Coca", 2.00, "Refreshing Coke", "image_url", 500),
    Beverage("Sprite", 2.00, "Lemon-lime flavored soft drink", "image_url", 500),
    Beverage("Water", 1.50, "Bottled mineral water", "image_url", 500)
]

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
def makeOrder():
    items = [pizzas[0], beverages[0]]
    current_time = datetime.now().strftime("%H:%M:%S")

    # Create an order instance
    order = Order(1, 4, current_time, items, sum(item.price for item in items), "TO DO")

    return jsonify(order.__dict__)

if __name__ == '__main__':
    app.run(port=8080)
