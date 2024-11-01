import uuid
from datetime import datetime as dt

class Order:
    STATUS_OPTIONS = ["TO DO", "COOKING", "READY FOR SERVING", "SERVED"]

    def __init__(self, table, products, totalPrice, status="TO DO", id=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.table = table
        self.datetime = dt.now()
        self.products = products
        self.totalPrice = totalPrice
        self.status = status

    def update_totalPrice(self):
        self.totalPrice = sum(item.price for item in self.products)

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

    def to_dict(self):
        return {
            "id": self.id,
            "table": self.table,
            "datetime": str(self.datetime),
            "products": [product.to_dict() for product in self.products],
            "totalPrice": self.totalPrice,
            "status": self.status
        }
