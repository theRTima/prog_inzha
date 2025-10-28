class MenuItem:
    def __init__(self, item_id, name, category, price, available, description=""):
        self.id = item_id
        self.name = name
        self.category = category
        self.price = price
        self.available = available
        self.description = description