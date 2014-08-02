#!/usr/bin/python
import item.item.item as item
import random as rnd

class ItemBlade(item.Item):
    def __init__(self):
        self.name = "Blade"
        self.cost = 2
    
    def setup(self, stack, tp): #Setup standard for a base item of class
        #MATERIAL
        if rnd.randint(0, 10) == 0 and 2 <= tp:
            stack.setInfo("Material", "Steel")
            tp -= 2
        elif rnd.randint(0, 10) == 0 and 4 <= tp:
            stack.setInfo("Material", "Silver")
            tp -= 4
        elif rnd.randint(0, 10) == 0 and 1 <= tp:
            stack.setInfo("Material", "Copper")
            tp -= 1
        else:
            stack.setInfo("Material", "Iron")
        #SIZE
        if rnd.randint(0, 5) == 0:
            stack.setInfo("Size", "2H-Sword")
        elif rnd.randint(0, 5) == 0:
            stack.setInfo("Size", "Shortsword")
        elif rnd.randint(0, 10) == 0:
            stack.setInfo("Size", "Sword")
        else:
            stack.setInfo("Size", "Dagger")
        #CROSS-GUARD
        
        #GRIP
        
        return tp
    
    def makeName(self, stack): #Name the item after features are added
        stack.name = stack.getInfo("Material") + " " + stack.getInfo("Size")
    
    def description(self, stack):
        return "How about... blades"