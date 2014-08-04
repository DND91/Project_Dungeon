#!/usr/bin/python

import random as rnd
import math

import entity.race.race_list as rcs
import entity.profession.profession_list as prfs
import item.generator as igen

'''

    Monster generation
    Dung Points(DP) = For buying a monster like we have Treasure points for Items.
    Monster = Entity + AI + Race + Profession + Inventory With Items
    Monster Generation want to work with Race, Profession and Inventory and give an abstract thought on what
    the AI should be (Brave, Coward, Berserker and so on).

'''

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

def generateMonster(dp, race_type  = "Random", profession_type = "Random", inventory_type = "Random", personality_type = "Random"):
    stats = dict()
    start_cost = dp
    #RACE
    if race_type == "Random":
        race = tryToBuyFrom(dp, rcs.races)
        dp -= race.getCost()
    else:
        for r in rcs.races:
            if r.getName() == race_type:
                race = r
                break
    stats["Race"] = race.getName()
    race.setup(stats)
    
    #PROFESSION
    if profession_type == "Random":
        profession = tryToBuyFrom(dp, prfs.professions)
        dp -= profession.getCost()
    else:
        for p in prfs.professions:
            if p.getName() == profession_type:
                profession = p
                break
    stats["Profession"] = profession.getName()
    profession.setup(stats)
    
    #INVENTORY, later date, Dummy values
    if inventory_type == "Random":
        tp = rnd.randint(0, dp)
        dp -= tp
        stats["Wearing"] = igen.generateItemStack(tp, 1)
        dp += tp - stats["Wearing"].cost
    else:
        x = 0
    
    #PERSONALITY(AI), later date, Dummy values
    if personality_type == "Random":
        race.makePersonality(stats)
    else:
        stats["Personality"] = personality_type
    
    #Entity is set outside of the generation.
    
    #MAKE DRAW
    race.makeDraw(stats)
    
    stats["Cost"] = start_cost - dp
    
    return stats