#!/usr/bin/python

import entity.monster.generator as mgen

for x in range(1):
    stats = mgen.generateMonster(50)
    print(stats)




