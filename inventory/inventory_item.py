class InventoryItem:

    def __init__(self, y, x, name):
        self.size = [y, x]
        self.flipped = False
        self.name = name

    def get_size(self):
        return self.size

    def get_name(self):
        return self.name

    def flip(self):
        self.size.reverse()
        self.flipped = not self.flipped
