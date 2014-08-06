class Inventory:
    
    def __init__(self, y, x):
        
        self._contents = {0: None}
        self._matrix = []
        self._size = [y, x]
        
        for y in range(self._size[0]):
            
            self._matrix.append([])

            for x in range(self._size[1]):
                self._matrix[y].append(0)

    @property
    def size(self):
        return self._size()

    @size.setter
    def size(self, value):
        self._size = value
        
    def get_item(self, key):
        return self._contents[key]

    def get_key(self, y, x):
        return self._matrix[y][x]

    def _out_of_bounds(self, coord, size):
        if (coord[0] + size[0] > self.size[0] or
            coord[1] + size[1] > self.size[1]):
            
            return True

        return False

    def _fit(self, coord, size):
        
        for y in range(coord[0], coord[0] + size[0]):
            for x in range(coord[1], coord[1] + size[1]):

                if self.get_item(self._matrix[y][x]) is not None:
                    return False
        
        return True

    def display_contents(self):
        print(self._contents)

    def _fill_matrix_rect(self, key, coord, size):

        for y in range(coord[0], coord[0] + size[0]):
            for x in range(coord[1], coord[1] + size[1]):

                self._matrix[y][x] = key

    def _get_first_free_key(self):
        
        key = 1
        
        while key in self._contents:
            key += 1

        return key

    def _get_last_used_key(self):
        
        return max(self._contents)

    def _add(self, item, coord):
        
        size = item.size

        if not self._out_of_bounds(coord, size):
            if self._fit(coord, size):
                
                key = self._get_first_free_key()
                self._contents[key] = item
                self._fill_matrix_rect(key, coord, size)

                return True

        return False

    def _remove(self, key):
   
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                
                if self._matrix[y][x] == key:
                    
                    self._matrix[y][x] = 0

        del self._contents[key]

    def fetch(self, key):
        item = self.get_item(key)
        if item is not None:
            self._remove(key)
        return item

    def put(self, coord, item):
        size = item.size

        if self._out_of_bounds(coord, size):
            return item

        if self._add(item, coord):
            return None
        else:

            for y in range(coord[0], coord[0] + size[0]):
                for x in range(coord[1], coord[1] + size[1]):

                    if self._matrix[y][x] != 0:
        
                        found = self.fetch(self._matrix[y][x])
                        if self._add(item, coord):
                            return found
                        else:
                            self._add(found, (y, x))
                            return item

    def _get_coordinate(self, key):

        for y in range(self.size[0]):
            for x in range(self.size[1]):
                
                if self._matrix[y][x] == key:
                    
                    return (y, x)

    def flip(self, key):
        
        item = self.get_item(key)
        coord = self._get_coordinate(key)

        self._remove(key)
        
        item.flip()

        if not self._add(item, coord):
            item.flip()
            self._add(item, coord)
            return False

        return True

    def pickup(self, item):
        
        for y in range(self.size[0]):
            for x in range(self.size[1]):

                if self._add(item, (y, x)):
                    return True
                else:
                    item.flip()

                    if self._add(item, (y, x)):
                        return True

        return False

    def display_matrix(self):
        length = self.size[1]
        spacing = max(3, len(str(self._get_last_used_key())))
        firsthalf = spacing // 2
        secondhalf = spacing - firsthalf
        bar = "+" + length * (spacing * "-" + "+")

        print(bar)

        for row in self._matrix:

            string = "|"

            for sign in row:
                string += (firsthalf * " " + str(sign) + 
                           (secondhalf - len(str(sign))) * " " + "|")
                
            print(string)
            print(bar)

