#!/usr/bin/python
import item.item.item_list as itms
import item.itemstack as its
import random as rnd
import item.coperation.coperation_list as cops
import math

def tryToBuyFrom(highest, lib, smallest = 0):
    candidate = lib.fetch()

    if smallest <= candidate.cost <= highest:
        return candidate
    return None

def generateItemStack(tp, amount, type = "Random",coop = None):
    startCost = tp
    #Item Class Chooice
    itemC = None
    if type == "Random":
        while itemC is None:
            itemC = tryToBuyFrom(tp, itms.items)
        tp -= itemC.cost
    else:
        for item in itms.items:
            if item.name == type:
                itemC = item
                break
    
    stack = its.ItemStack(itemC, amount)
    
    #Item Setup and Leftovers...
    tp = itemC.generate(stack, tp)
    
    stack.cost = startCost - tp
    
    #Setup Item Name, Move to setup?
    itemC.makeName(stack)
    
    #Setup Coperation
    if coop == None and 5 <= stack.cost:
        cops.randomCoop(stack)
    #else:#Hook place for if players make thier own cooperation...
    #    stack.name = coop + " " + stack.name
    
    return stack





















