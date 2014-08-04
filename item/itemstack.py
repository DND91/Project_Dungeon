#!/usr/bin/python

class ItemStack:
    
    def __init__(self, itemC, amount):
        self.name = "Item"
        self.itemC = itemC
        self.amount = amount
        self.info = dict()
        self.cost = 0
    
    def __str__(self):
        return "ItemStack." + self.itemC.name + "(" + self.name + ", amount " + str(self.amount) + ", cost " + str(self.cost) + ", " + self.info.__str__()
    
    def __repr__(self):
        return self.__str__()
    
    def description(self):
        return self.itemC.description(self)
    
    def getInfo(self, tag):
        return self.info[tag]
    
    def setInfo(self, tag, data):
        self.info[tag] = data
    
    def hasTag(self, tag):
        return tag in self.info
    