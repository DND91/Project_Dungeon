class AbstractRoom:

    def __init__(self):
        self.coords = []
        self.connects = []

    def add_coord(self, y, x):
        self.coords.append((y, x))

    def contains(self, y, x):
        if (y, x) in self.coords:
            return True
        return False

    def connect(self, key):
        self.connects.append(key)

    def disconnect(self, key):
        self.connects.remove(key)

    def is_connected(self, key):
        if key in self.connects:
            return True
        return False

    def get_coords(self):
        return self.coords

    def get_connects(self):
        return self.connects

    
        
