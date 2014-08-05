class Inventory:
    
    def __init__(self, y, x):
        
        self.contents = {0: None}
        self.matrix = []
        self.size = [y, x]
        
        for y in range(self.size[0]):
            
            self.matrix.append([])

            for x in range(self.size[1]):
                self.matrix[y].append(0)

    def get_item(self, key):
        return self.contents[key]

    def get_key(self, y, x):
        return self.matrix[y][x]

    def out_of_bounds(self, coord, size):
        if (coord[0] + size[0] > self.size[0] or
            coord[1] + size[1] > self.size[1]):
            
            return True

        return False

    def fit(self, coord, size):
        
        for y in range(coord[0], coord[0] + size[0]):
            for x in range(coord[1], coord[1] + size[1]):

                if self.get_item(self.matrix[y][x]) is not None:
                    return False
        
        return True

    def display_contents(self):
        print(self.contents)

    def fill_matrix_rect(self, key, coord, size):

        for y in range(coord[0], coord[0] + size[0]):
            for x in range(coord[1], coord[1] + size[1]):

                self.matrix[y][x] = key

    def get_first_free_key(self):
        
        key = 1
        
        while key in self.contents:
            key += 1

        return key

    def get_last_used_key(self):
        
        return max(self.contents)

    def add_item(self, item, coord):
        
        size = item.get_size()

        if not self.out_of_bounds(coord, size):
            if self.fit(coord, size):
                
                key = self.get_first_free_key()
                self.contents[key] = item
                self.fill_matrix_rect(key, coord, size)

                return True

        return False

    def remove_item(self, key):
   
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                
                if self.matrix[y][x] == key:
                    
                    self.matrix[y][x] = 0

        del self.contents[key]

    def fetch(self, key):
        item = self.get_item(key)
        if item is not None:
            self.remove_item(key)
        return item

    def put(self, coord, item):
        size = item.get_size()

        if self.out_of_bounds(coord, size):
            return item

        if self.add_item(item, coord):
            return None
        else:

            for y in range(coord[0], coord[0] + size[0]):
                for x in range(coord[1], coord[1] + size[1]):

                    if self.matrix[y][x] != 0:
        
                        found = self.fetch(self.matrix[y][x])
                        if self.add_item(item, coord):
                            return found
                        else:
                            return item

    def get_coordinate(self, key):

        for y in range(self.size[0]):
            for x in range(self.size[1]):
                
                if self.matrix[y][x] == key:
                    
                    return (y, x)

    def flip(self, key):
        
        item = self.get_item(key)
        coord = self.get_coordinate(key)

        self.remove_item(key)
        
        item.flip()

        if not self.add_item(item, coord[0], coord[1]):
            item.flip()
            self.add_item(item, coord[0], coord[1])
            return False

        return True

    def pickup(self, item):
        
        for y in range(self.size[0]):
            for x in range(self.size[1]):

                if self.add_item(item, (y, x)):
                    return True
                else:
                    item.flip()

                    if self.add_item(item, (y, x)):
                        return True

        return False

    def display_matrix(self):
        length = self.size[1]
        spacing = max(3, len(str(self.get_last_used_key())))
        firsthalf = spacing // 2
        secondhalf = spacing - firsthalf
        bar = "+" + length * (spacing * "-" + "+")

        print(bar)

        for row in self.matrix:

            string = "|"

            for sign in row:
                string += (firsthalf * " " + str(sign) + 
                           (secondhalf - len(str(sign))) * " " + "|")
                
            print(string)
            print(bar)

