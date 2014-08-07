#!/usr/bin/python

class ItemStack:
    
    def __init__(self, item, amount):
        self._name = "Item"
        self._item = item
        self._amount = amount
        self._info = {}
        self._cost = 0
        self._weight = 1
        self._flipped = False

    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def item(self):
        return self._item

    @property
    def amount(self):
        return self._amount

    @property
    def info(self):
        return self._info

    @property
    def size(self):
        return self.info["size"]

    @property
    def slot(self):
        return self.info["equip"]

    @property
    def weight(self):
        return self._weight

    def flip(self):
        self.size.reverse()
        self._flipped = not self._flipped
    
    def __str__(self):
        return "ItemStack." + self.item.name + "(" + self.name + ", amount " + str(self.amount) + ", cost " + str(self.cost) + ", " + self.info.__str__()
    
    def __repr__(self):
        return self.__str__()
    
    def description(self):
        return self.item.description(self)
    
    def hasTag(self, tag):
        return tag in self.info
    
