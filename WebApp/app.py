from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'DoughminatorsKey'

pizzas = [
    {"name": "Margherita", "price": 8.00, "description": "Classic cheese and tomato pizza"},
    {"name": "Pepperroni","price": 9.50, "description": "Pepperoni with mozzarella cheese"},
    {"name": "Veggie", "price": 9.00, "description": "Bell peppers, olives, onions and tomatoes"}
]
beverages = [
    {"name": "Cola-Coca", "price": 2.00, "description": "Refreshing Coke"},
    {"name": "Sprite","price": 2.00, "description": "Lemon-lime flalvored soft drink"},
    {"name": "Water", "price": 1.50, "description": "Bottled mineral water"}
]
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/pizza")
def pizza_page():
    return render_template('pizza.html',pizzas=pizzas)

@app.route("/beverages")
def beverages_pages():
    return render_template('beverages.html', beverages = beverages)

if __name__ == '__main__':
    app.run(port=8080)