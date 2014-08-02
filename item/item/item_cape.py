#!/usr/bin/python
import item.item.item as item
import random as rnd

class ItemCape(item.Item):
    def __init__(self):
        self.name = "Cape"
        self.cost = 2
    
    def setup(self, stack, tp): #Setup standard for a base item of class
        #MATERIAL
        if rnd.randint(0, 10) == 0 and 2 <= tp:
            stack.setInfo("Material", "Leaf")
            tp -= 2
        elif rnd.randint(0, 10) == 0 and 4 <= tp:
            stack.setInfo("Material", "Spidersilk")
            tp -= 4
        elif rnd.randint(0, 10) == 0 and 1 <= tp:
            stack.setInfo("Material", "Wool")
            tp -= 1
        else:
            stack.setInfo("Material", "Rags")
        return tp
    
    def makeName(self, stack): #Name the item after features are added
        stack.name = stack.getInfo("Material") + " " + self.getName()
    
    def description(self, stack):
        return "How about... Cape"