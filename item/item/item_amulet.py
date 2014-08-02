#!/usr/bin/python
import item.item.item as item
import random as rnd

class ItemAmulet(item.Item):
    def __init__(self):
        self.name = "Amulet"
        self.cost = 0
    
    def setup(self, stack, tp): #Setup standard for a base item of class
        if rnd.randint(0, 10) == 0 and 5 <= tp:
            stack.setInfo("Base", "Gold")
            tp -= 5
        elif rnd.randint(0, 10) == 0:
            stack.setInfo("Base", "Silver")
        elif rnd.randint(0, 5) == 0:
            stack.setInfo("Base", "Copper")
        else:
            stack.setInfo("Base", "Stone")
        return tp
    
    def makeName(self, stack): #Name the item after features are added
        stack.name = stack.getInfo("Base") + " " + self.getName()
    
    def description(self, stack):
        return "How about... Amulet"