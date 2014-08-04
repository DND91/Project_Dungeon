#!/usr/bin/python
import functools

professions = []

#IMPORT PROFESSIONS
import entity.profession.farmer
import entity.profession.hunter
import entity.profession.warrior

#INIT PROFESSIONS
farmer = entity.profession.farmer.Farmer()
hunter = entity.profession.hunter.Hunter()
warrior = entity.profession.warrior.Warrior()

#APPEND PROFESSIONS
professions.append(farmer)
professions.append(hunter)
professions.append(warrior)

#SORT LIST
def compare(a, b):
    return a.getCost() - b.getCost()
professions = sorted(professions, key=functools.cmp_to_key(compare))