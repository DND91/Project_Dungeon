class EquipmentSlot:
    
    def __init__(self, *types):
        self._types = types
        self._content = None

    @property
    def content(self):
        return self._content

    def _valid(self, item):

        if (any(slot in item.slots for slot in self._types)):
            return True

        return False

    def empty(self):
        if self.content is None:
            return True
        return False

    def fill(self, item):
        # Only use this method privately or on the "Active" slot!
        self._content = item

    def _clear(self):
        self._content = None

    def fetch(self):
        item = self.content
        self._clear()
        return item

    def equip(self, item):
        
        if not self._valid(item):
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
            print(self._content.get_name())
