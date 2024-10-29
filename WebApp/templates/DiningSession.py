class DiningSession:
    def __init__(self, id, table, orders, is_open):
        self.id = id
        self.table = table
        self.orders = orders
        self.is_open = is_open

    def add_order(self, order):
        if self.is_open:
            self.orders.append(order)
        else:
            raise ValueError("Cannot add order to a closed session")

    def close_session(self):
        self.is_open = False

    def calculate_total(self):
        return sum(order.calculate_total() for order in self.orders if order.status != "delivered")

    def to_dict(self):
        return {
            "id": self.id,
            "table": self.table,
            "orders": [order.to_dict() for order in self.orders],
            "is_open": self.is_open
        }