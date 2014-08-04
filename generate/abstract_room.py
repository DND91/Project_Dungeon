class AbstractRoom:

    def __init__(self):
        self.coords = []
        self.connects = []
        self.paths = {}

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

    def get_paths(self):
        return self.paths

    def add_path(self, dst, path):
        self.paths[dst] = path

    def get_abstract_distance(self, dst):
        return self.paths[dst].get_length()

    def setup_room_properties(self):
        

class AbstractPath:

    def __init__(length, path):
        self.length = length
        self.path = path

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def set_length(self, length):
        self.length = length

    def get_length(self):
        return self.length

    
        
