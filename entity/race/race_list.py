#!/usr/bin/python
import functools

races = []
#IMPORT RACES
import entity.race.human
import entity.race.orc
import entity.race.skeleton

#INIT RACES
human = entity.race.human.Human()
orc = entity.race.orc.Orc()
skeleton = entity.race.skeleton.Skeleton()

#APPEND RACES
races.append(human)
races.append(orc)
races.append(skeleton)

#SORT LIST
def compare(a, b):
    return a.getCost() - b.getCost()
races = sorted(races, key=functools.cmp_to_key(compare))


