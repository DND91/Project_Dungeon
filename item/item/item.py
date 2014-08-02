#!/usr/bin/python

class Item:
    def __init__(self):
        self.name = "Standard"
        self.cost = 0
    
    def __str__(self):
        return "Item." + self.name
    
    def __repr__(self):
        return self.__str__()
    
    def getName(self):
        return self.name
    
    def getCost(self):
        return self.cost
    
    def description(self, stack):
        return "How about no..."
    
    def heldDraw(self, stack): #NOT HOOKED
        return None
    
    def groundDraw(self, stack): #NOT HOOKED
        return None
    
    #SETUP
    
    def setup(self, stack, tp): #Setup standard for a base item
        return tp
    
    def makeName(self, stack): #Name the item before giving it to coperations
        stack.name = "Standard_No_Name_Missing_No_98"
    
    #ITEM HOOKS
    
    def wearing(self, stack, slot): #NOT HOOKED
        x = 0
    
    def inventory(self, stack, slot): #NOT HOOKED
        x = 0
    
    def onGround(self, stack, ent): 
        x = 0
    
    def use(self, stack): #NOT HOOKED
        x = 0
    
    def held(self, stack, slot): #NOT HOOKED
        x = 0
    
    def attack(self, user, stack, enemy): #NOT HOOKED
        x = 0






















