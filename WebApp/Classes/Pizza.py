from .Product import Product



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
