from datetime import datetime

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
