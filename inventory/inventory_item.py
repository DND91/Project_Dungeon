class InventoryItem:

    def __init__(self, y, x, name, weight, *slots):
        self._size = [y, x]
        self._flipped = False
        self._name = name
        self._weight = weight
        self._slots = slots

    @property
    def size(self):
        return self._size

    @property
    def weight(self):
        return self._weight

    @property
    def name(self):
        return self._name

    @property
    def slots(self):
        return self._slots

    def flip(self):
        self._size.reverse()
        self._flipped = not self._flipped
