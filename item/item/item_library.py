import random as rnd

class ItemLibrary:
    
    def __init__(self):
        self._contents = {}
        self._total_weight = 0

    def fill(self, *args):
        for base in args:
            self._contents[range(self._total_weight, 
                                 self._total_weight + base.occurence)] = base
            self._total_weight += base.occurence
            
    def fetch(self):
        index = rnd.randint(0, self._total_weight - 1)

        for key in self._contents:
            if index in key:
                return self._contents[key]
