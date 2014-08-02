#!/usr/bin/python
import item.item.item_list as itms
import item.itemstack as its
import random as rnd
import item.coperation.coperation_list as cops
import math

def tryToBuyFrom(highest, l, smallest = 0):
    first = 0
    last = 0
    for indx, elm in reversed(list(enumerate(l))):
        if elm.getCost() <= highest:
            last = indx + 1
            break
    
    for indx, elm in enumerate(l):
        if smallest <= elm.getCost():
            first = indx
            break
    
    return rnd.choice(l[first:last])

def generateItemStack(tp, amount, type = "Random",coop = None):
    startCost = tp
    #Item Class Chooice
    itemC = 0
    if type == "Random":
        itemC = tryToBuyFrom(tp, itms.items)
        tp -= itemC.getCost()
    else:
        for item in itms.items:
            if item.getName() == type:
                itemC = item
                break
    
    stack = its.ItemStack(itemC, amount)
    
    #Item Setup and Leftovers...
    tp = itemC.setup(stack, tp)
    
    stack.cost = startCost - tp
    
    #Setup Item Name, Move to setup?
    itemC.makeName(stack)
    
    #Setup Coperation
    if coop == None and 5 <= stack.cost:
        cops.randomCoop(stack)
    #else:#Hook place for if players make thier own cooperation...
    #    stack.name = coop + " " + stack.name
    
    return stack





















