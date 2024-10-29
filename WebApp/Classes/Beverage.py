from .Product import Product


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
