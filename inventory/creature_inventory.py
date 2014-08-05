from inventory import *
from equipment_slot import *

class CreatureInventory:

    base_size = (3, 2)
    
    def __init__(self):
        
        self.active = EquipmentSlot("any")
        self.slots = {"Amulet": EquipmentSlot("amulet"),
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
                      "Hands": [EquipmentSlot("weapon"), 
                                EquipmentSlot("weapon", "shield")],
                      "Headgear": EquipmentSlot("headgear"),
                      "Misc": [EquipmentSlot("misc")],
                      "Quick_use": [],
                      "Quiver": [],
                      "Rings": [EquipmentSlot("ring"), 
                                EquipmentSlot("ring")],
                      "Shirt": EquipmentSlot("shirt")}
        
        self.inv = Inventory(self.base_size[0], self.base_size[1])
        self.weight = 0

    def pickup(self, item):
        if self.inv.pickup(item):
            self.weight += item.get_weight()
            return True
        return False

    def active_taken(self):
        if self.slots["Active"].empty():
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
        self.weight -= slot.fetch().get_weight()

    def throw_away_from_inv(self, y, x):
        self.weight -= self.inv.fetch(self.inv.get_key(y, x)).get_weight()

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
