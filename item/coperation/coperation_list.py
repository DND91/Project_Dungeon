#!/usr/bin/python
import random as rnd
import item.coperation.coperation_the_neutral as neutral
import item.coperation.coperation_chaos as choas
import item.coperation.coperation_elven_stone as elven_stone

coperations = []

def randomCoop(stack):
    cope = rnd.choice(coperations)
    cope.setupStack(stack)

#APPEND COPS
coperations.append(neutral.TheNeutralCoperation())
coperations.append(choas.ChaosCoperation())
coperations.append(elven_stone.ElvenStoneCoperation())
