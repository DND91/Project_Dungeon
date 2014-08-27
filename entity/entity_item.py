#!/usr/bin/python
import sfml as sf
from math import *
from world.isometric_tile import *
from world.cool_phys import *
from entity import entity

class ItemEntity(entity.Entity):
    name = "ITEM_ENTITY"
    
    def __init__(self, world, x, y, game, stack):
        super().__init__("ITEM_TILE", world, x, y, 64,64)
        self.body.mass = 1
        self.moviable = False
        self.solid = False
        self.stack = stack
    
    def update(self, game, delta):
        super().update(game, delta)
        self.stack.itemC.onGround(self.stack, self)
    
    def draw(self, game):
        self.visPos = worldToScreen(sf.Vector2(self.body.rectangle.left+64, self.body.rectangle.top+64))
        self.count += 1
        self.anibase.draw(self.animation, self.action, self.count, self.visPos.x, self.visPos.y, game.window)
    
    def mouseClick(self, game):
        print(self.stack.name)
