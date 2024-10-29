from flask import Flask, render_template, jsonify
from datetime import datetime

from Classes.Topping import *





# class Topping:
#     def __init__(self, name, price, description=""):
#         self.name = name
#         self.price = price
#         self.description = description

#     def to_dict(self):
#         return {
#             "name": self.name,
#             "price": self.price,
#             "description": self.description
#         }

class Product:
    def __init__(self, name, price, description, imageURL):
        self.name = name
        self.price = price
        self.description = description
        self.imageURL = imageURL

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "imageURL": self.imageURL
        }


class Pizza(Product):
    def __init__(self, name, price, description, imageURL, crust, base, size, toppings):
        super().__init__(name, price, description, imageURL)
        self.crust = crust
        self.base = base
        self.size = size
        self.toppings = toppings

    def add_topping(self, topping):
        self.toppings.append(topping)
        self.price += topping.price

    def remove_topping(self, topping):
        if topping in self.toppings:
            self.toppings.remove(topping)
            self.price -= topping.price

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "imageURL": self.imageURL,
            "crust": self.crust,
            "base": self.base,
            "size": self.size,
            "toppings": [topping.to_dict() for topping in self.toppings]
        }



class Beverage(Product):
    def __init__(self, name, price, description, imageURL, milliliters):
        super().__init__(name, price, description, imageURL)
        self.milliliters = milliliters

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "imageURL": self.imageURL,
            "milliliters": self.milliliters
        }


class Order:
    STATUS_OPTIONS = ["TO DO", "COOKING", "READY FOR SERVING", "SERVED"]
    def __init__(self, id, table, datetime, products, totalPrice, status):
        self.id = id
        self.table = table
        self.datetime = datetime.now()
        self.products = products
        self.totalPrice = totalPrice
        self.status = "TO DO"

    def update_totalPrice(self):
        totalPrice = sum(item.price for item in self.products)

    def add_product(self, product):
        self.products.append(product)
        self.totalPrice += product.price

    def remove_product(self, product):
        self.products.remove(product)
        self.totalPrice -= product.price

    def set_status(self, status):
        if status in self.STATUS_OPTIONS:
            self.status = status
        else:
            raise ValueError("Status must be one of: " + ", ".join(self.STATUS_OPTIONS))

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
    items = [pizzas[0], beverages[0]]  # Add one pizza and one beverage to the order
    current_time = datetime.now().strftime("%H:%M:%S")

    # Create an order instance
    order = Order(1, 4, current_time, items, sum(item.price for item in items), "TO DO")

    return jsonify(order.__dict__)  # Convert the order object to JSON

if __name__ == '__main__':
    app.run(port=8080)
