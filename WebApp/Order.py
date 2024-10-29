from datetime import datetime

class Order:
    def __init__(self, table, datetime, products, totalPrice):
        self.table = table
        self.datetime = datetime.now()
        self.products = products
        self.totalPrice = totalPrice
