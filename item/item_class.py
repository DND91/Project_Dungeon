#!/usr/bin/python

classes = []

class ItemClass:
    
    def __init__(self, name, cost, parts):
        self.name = name
        self.cost = cost
        self.parts = parts
        classes.append(self)
    
    def __str__(self):
        return "ItemClass." + self.name + "(" + self.parts.__str__() + ")"
    
    def __repr__(self):
        return self.__str__()
    
    def setup(self, stack, tp):
        x = 0
        return tp
    
    def makeName(self, stack):
        stack.name = self.name
    
    def description(self, stack):
        des = stack.name + "\n"
        for part in self.parts:
            feat = stack.info[part]
            if feat == None:
                des += "Simpel " + part
            else:
                des += feat.description(part)
            des += "\n"
        return des

class AmuletClass(ItemClass):
    def __init__(self, name, cost, parts):
        super().__init__(name, cost, parts)



class ItemClasses:
    
    #ARMOUR
    #helmet = ItemClass("Helmet", 1, ["Decor", "Side", "Side", "Top"])
    amulet = AmuletClass("Amulet", 0, ["Decor", "Base", "Chain", "Lock"])
    #shoulders = ItemClass("Shoulders", 1, ["Decor", "Padding"])
    #cape = ItemClass("Cape", 4, ["Decor", "Hang", "Cloth", "Bottom"])
    #chest = ItemClass("Chest", 4, ["Decor", "Front", "Back", "Stomach"])
    #belt = ItemClass("Belt", 0, ["Decor", "Strap", "Buckel"])
    #legs = ItemClass("Legs", 2, ["Decor", "Front", "Back"])
    #feet = ItemClass("Feet", 1, ["Decor", "Bottom", "Front", "Neck"])
    #arm = ItemClass("Arm", 1, ["Decor", "Base", "Strap"])
    #gloves = ItemClass("Gloves", 0, ["Decor", "Base"])
    
    #WEAPONS
    #Just make it bigger or smaller to create daggers or swords. A blade is always a blade.
    #blade = ItemClass("Blade", 0, ["Decor", "Blade", "Cross-guard", "Grip", "Pommel"])
    #club = ItemClass("Club", 4, ["Decor", "Grip", "Club-head", "Club-body"])
    
    #POTIONS
    
    
    #MISC
    
    
    
    def __init__(self):
        self.text = "I Like Spageti"
itemClasses = ItemClasses()

