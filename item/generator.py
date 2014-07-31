#!/usr/bin/python
import item.feature as fea
import item.item_class as itc
import item.itemstack as its
import random as rnd
import item.coperation as cop

def tryToBuyFrom(tp, list):
    for x in range(0, 10):
        ent = rnd.choice(list)
        if ent.cost <= tp:
            return ent
    return None

def generateItemStack(tp, amount, coop = None):
    startCost = tp
    #Item Class Chooice
    itemC = tryToBuyFrom(tp, itc.classes)
    if itemC == None:
        return itemC
    else:
        tp -= itemC.cost
    
    stack = its.ItemStack(itemC, amount)
    
    #Item Class Setup and Cost
    tp = itemC.setup(stack, tp)
    
    #Init Features
    for part in itemC.parts:
        if part in fea.features:
            feat = tryToBuyFrom(tp, fea.features[part])
            if not (feat == None):
                stack.info[part] = feat
                tp -= feat.cost
    
    stack.cost = startCost - tp
    
    #Setup Basic Item Name
    itemC.makeName(stack)
    
    #Setup Coperation Name and creator
    if coop == None:
        cop.randomCoop(stack)
    else:#Hook place for if players make thier own cooperation...
        stack.name = coop + " " + stack.name
    
    return stack





















