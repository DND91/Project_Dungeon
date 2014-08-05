class InventoryItem:

    def __init__(self, y, x, name, weight, *slots):
        self.size = [y, x]
        self.flipped = False
        self.name = name
        self.weight = weight
        self.slots = slots

    def get_size(self):
        return self.size

    def get_weight(self):
        return self.weight

    def get_name(self):
        return self.name

    def flip(self):
        self.size.reverse()
        self.flipped = not self.flipped

    def get_slots(self):
        return self.slots
