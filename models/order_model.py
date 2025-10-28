class Order:
    def __init__(self, order_id, customer, phone, status, created, notes=""):
        self.id = order_id
        self.customer = customer
        self.phone = phone
        self.status = status
        self.created = created
        self.notes = notes
        self.items = []
        self.total = 0

    def add_item(self, dish, quantity, price):
        item_total = quantity * price
        self.items.append({
            'dish': dish,
            'quantity': quantity,
            'price': price,
            'total': item_total
        })
        self.total += item_total

    def calculate_total(self):
        self.total = sum(item['total'] for item in self.items)
        return self.total