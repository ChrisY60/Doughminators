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
