from inventory.inventory import *
from inventory.equipment_slot import *

class CreatureInventory:

    base_size = (5, 2)
    
    def __init__(self):
        
        self._active = EquipmentSlot()
        self._slots = {"Amulet": EquipmentSlot("amulet"),
                      "Backpack": EquipmentSlot("backpack"),
                      "Belt": EquipmentSlot("belt"),
                      "Boots": EquipmentSlot("boots"),
                      "Bracelets": [EquipmentSlot("bracelet"), 
                                    EquipmentSlot("bracelet")],
                      "Cape": EquipmentSlot("cape"),
                      "Chestpiece": EquipmentSlot("chestpiece"),
                      "Containers" : [],
                      "Earrings": EquipmentSlot("earrings"),
                      "Gauntlets": EquipmentSlot("gauntlets"),
                      "Greaves": EquipmentSlot("greaves"),
                       "Hands": [EquipmentSlot("1_hand", "2_hand"), 
                                 EquipmentSlot("1_hand", "shield")],
                      "Headgear": EquipmentSlot("headgear"),
                      "Misc": [EquipmentSlot("misc")],
                      "Quick_use": [],
                      "Quiver": [],
                      "Rings": [EquipmentSlot("ring"), 
                                EquipmentSlot("ring")],
                      "Shirt": EquipmentSlot("shirt")}
        
        self._inv = Inventory(self.base_size[0], self.base_size[1])
        self._weight = 0

    @property
    def active(self):
        return self._active

    @property
    def amulet(self):
        return self._slots["Amulet"]

    @property
    def belt(self):
        return self._slots["Belt"]

    @property
    def boots(self):
        return self._slots["Boots"]

    @property
    def bracelets(self):
        return self._slots["Bracelets"]

    @property
    def cape(self):
        return self._slots["Cape"]

    @property
    def chestpiece(self):
        return self._slots["Chestpiece"]

    @property
    def containers(self):
        return self._slots["Containers"]

    @property
    def earrings(self):
        return self._slots["Earrings"]

    @property
    def gauntlets(self):
        return self._slots["Gauntlets"]

    @property
    def greaves(self):
        return self._slots["Greaves"]

    @property
    def hands(self):
        return self._slots["Hands"]

    @property
    def headgear(self):
        return self._slots["Headgear"]

    @property
    def misc(self):
        return self._slots["Misc"]

    @property
    def quick_use(self):
        return self._slots["Quick_use"]

    @property
    def quiver(self):
        return self._slots["Quiver"]

    @property
    def rings(self):
        return self._slots["Rings"]

    @property
    def shirt(self):
        return self._slots["Shirt"]

    @property
    def inv(self):
        return self._inv

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def slots(self):
        return self._slots

    def flip_active(self):
        self.active.content.flip()

    def pickup(self, item):
        if self.inv.pickup(item):
            self.weight += item.weight
            return True
        return False

    def active_taken(self):
        if self.active.empty():
            return False
        return True

    def take_from_slot(self, slot):
        self.active.fill(slot.fetch())
        
    def take_from_inv(self, y, x):
        self.active.fill(self.inv.fetch(self.inv.get_key(y, x)))

    def drop_on_slot(self, slot):
        self.active.fill(slot.equip(self.active.fetch()))

    def drop_in_inv(self, y, x):
        self.active.fill(self.inv.put((y, x), self.active.fetch()))

    def throw_away_from_slot(self, slot):
        self.weight -= slot.fetch().weight

    def throw_away_from_inv(self, y, x):
        self.weight -= self.inv.fetch(self.inv.get_key(y, x)).weight

    def display(self):
        print("EQUIPMENT:")
        
        for key, slotgrp in self.slots.items():
            print(key + ":")
            
            if isinstance(slotgrp, list):
                for slot in slotgrp:
                    slot.display()
            else:
                slotgrp.display()

        print("\nINVENTORY:")

        self.inv.display_matrix()

        print("\nWEIGHT CARRIED: " + str(self.weight))
