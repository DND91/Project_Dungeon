class EquipmentSlot:
    
    def __init__(self, *types):
        self.types = types
        self.content = None

    def valid(self, item):

        if (len(item.get_slots()) == 0 or 
            len(self.types) == 0 or
            any(slot in item.get_slots() for slot in self.types)):
            return True

        return False

    def empty(self):
        if self.content is None:
            return True
        return False

    def fill(self, item):
        # Only use this method privately or on the "Active" slot!
        self.content = item

    def _clear(self):
        self.content = None

    def examine(self):
        return self.content

    def fetch(self):
        item = self.content
        self._clear()
        return item

    def equip(self, item):
        
        if not self.valid(item):
            return item

        old_equip = None
        
        if not self.empty():
            old_equip = self.fetch()

        self.fill(item)

        return old_equip
        
    def display(self):
        if self.empty():
            print("nothing")
        else:
            print(self.examine().get_name())
