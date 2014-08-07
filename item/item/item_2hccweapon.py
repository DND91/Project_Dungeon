#!/usr/bin/python
import item.item.item_ccweapon as wpn
import item.item.item_library as lib
import item.item.item_base_type as base

class Item2HCCWeapon(wpn.ItemCCWeapon):
    def __init__(self, occurence):
        super().__init__(occurence)
        
        self._name = "2_handed_close_combat_weapon"
        self._cost = 2
        self._variant_lib = lib.ItemLibrary()

        #BELOW, WE DEFINE WHAT IS AVAILABLE IN THE LIBRARY
        self._variant_lib.fill(base.ItemBaseType("great axe", 3, 1, 
                                                 type = "axe",
                                                 size = [4, 2]),

                               base.ItemBaseType("zweihander", 2, 2, 
                                                 type = "sword",
                                                 size = [5, 2]),

                               base.ItemBaseType("great hammer", 3, 1, 
                                                 type = "hammer",
                                                 size = [4, 2]),

                               base.ItemBaseType("great sword", 3, 1, 
                                                 type = "sword",
                                                 size = [5, 1]),

                               base.ItemBaseType("great club", 4, 0, 
                                                 type = "club",
                                                 size = [4, 2]),

                               base.ItemBaseType("dai katana", 1, 3, 
                                                 type = "sword",
                                                 size = [5, 2])
                               )
        
    
    def generate(self, stack, tp):

        # STATIC_STUFF
        stack.info["equip"] = "2_hand"
        
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
        return "How about... 2 handed weapons"
