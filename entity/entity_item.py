#!/usr/bin/python
import sfml as sf
from math import *
from world.isometric_tile import *
from world.cool_phys import *
from entity import entity

class ItemEntity(entity.Entity):
    name = "ITEM_ENTITY"
    
    def __init__(self, world, x, y, game, stack):
        super().__init__(world, x, y, 64,64)
        texture = game.textures.fetch("ITEM_TILE")
        self.sprite = sf.Sprite(texture)
        self.sprite.position = self.body.rectangle.position
        self.body.mass = 1
        self.moviable = False
        self.solid = False
        self.stack = stack
    
    def update(self, game, delta):
        super().update(game, delta)
        self.stack.itemC.onGround(self.stack, self)
    
    def draw(self, ps, game):
        if ps == 1:
            tempPos = worldToScreen(sf.Vector2(self.body.rectangle.left+64, self.body.rectangle.top+64))
            self.sprite.position = tempPos
            game.window.draw(self.sprite)
    
    def mouseClick(self, game):
        print(self.stack.name)
