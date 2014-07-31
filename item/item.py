#!/usr/bin/python

class ItemClass:
    
    def __init__(self, name, parts):
        self.name = name
        self.parts = parts

class ItemClasses:
    
    #ARMOUR
    helmet = ItemClass("Helmet", ["Decor", "Side", "Side", "Top"])
    amulet = ItemClass("Amulet", ["Decor", "Base", "Chain", "Lock"])
    shoulders = ItemClass("Shoulders", ["Decor", "Padding"])
    cape = ItemClass("Cape", ["Decor", "Hang", "Cloth", "Bottom"])
    chest = ItemClass("Chest", ["Decor", "Front", "Back", "Stomach"])
    belt = ItemClass("Belt", ["Decor", "Strap", "Buckel"])
    legs = ItemClass("Legs", ["Decor", "Front", "Back"])
    feet = ItemClass("Feet", ["Decor", "Bottom", "Front", "Neck"])
    arm = ItemClass("Arm", ["Decor", "Base", "Strap"])
    gloves = ItemClass("Gloves", ["Decor", "Base"])
    
    #WEAPONS
    #Just make it bigger or smaller to create daggers or swords. A blade is always a blade.
    blade = ItemClass("Blade", ["Decor", "Blade", "Cross-guard", "Grip", "Pommel"])
    club = ItemClass("Club", ["Decor", "Grip", "Club-head", "Club-body"])
    
    #POTIONS
    
    
    #MISC
    
    
    
    def __init__(self):
        self.text = "I Like Spageti"
itemClasses = ItemClasses()

