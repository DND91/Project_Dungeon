#!/usr/bin/python
import item.item.item_ccweapon as wpn
import item.item.item_library as lib
import item.item.item_base_type as base

class Item1HCCWeapon(wpn.ItemCCWeapon):
    def __init__(self, occurence):
        super().__init__(occurence)

        self._name = "1_handed_close_combat_weapon"
        self._cost = 1
        self._variant_lib = lib.ItemLibrary()

        #BELOW, WE DEFINE WHAT IS AVAILABLE IN THE LIBRARY
        self._variant_lib.fill(base.ItemBaseType("battle axe", 2, 2, 
                                                 type = "axe",
                                                 size = [4, 2]),

                               base.ItemBaseType("shortsword", 3, 1, 
                                                 type = "sword",
                                                 size = [3, 1]),

                               base.ItemBaseType("longsword", 2, 2, 
                                                 type = "sword",
                                                 size = [4, 1]),

                               base.ItemBaseType("bastard sword", 1, 3, 
                                                 type = "sword",
                                                 size = [4, 1]),

                               base.ItemBaseType("gladius", 3, 1, 
                                                 type = "sword",
                                                 size = [3, 1]),

                               base.ItemBaseType("katana", 1, 3, 
                                                 type = "sword",
                                                 size = [4, 1])
                               )
    
    def generate(self, stack, tp): #Setup standard for a base item of class

        # STATIC_STUFF
        stack.info["equip"] = "1_hand"
        
        # GENERATION
        while True:
            candidate = self._variant_lib.fetch()
            if candidate.cost <= tp:
                tp -= candidate.cost
                stack.info["variant"] = candidate.name
                for key, value in candidate.stats.items():
                    stack.info[key] = value
                break
        
        return super().generate(stack, tp)
    
    def description(self, stack):
        return "How about... 1 handed weapons"
