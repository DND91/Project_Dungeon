#!/usr/bin/python
import entity.entity as entity
import sfml as sf
from math import *
from world.isometric_tile import *
from world.cool_phys import *

class MonsterEntity(entity.Entity):
    name = "MONSTERENTITY"
    
    def __init__(self, world, x, y, game, stats):
        super().__init__(stats["Texture"], world, x, y, 64,64)
        self.body.mass = 1000
        self.moviable = False
        self.stats = stats
    
    def mouseClick(self, game):
        print(self.stats)