#!/usr/bin/python
import entity.entity as entity
import sfml as sf
from math import *
from world.isometric_tile import *
from world.cool_phys import *

class MonsterEntity(entity.Entity):
    name = "MONSTERENTITY"
    
    def __init__(self, world, x, y, game, stats):
        super().__init__(world, x, y, 64,64)
        texture = game.textures.fetch(stats["Texture"])
        self.sprite = sf.Sprite(texture)
        self.sprite.position = self.body.rectangle.position
        self.body.mass = 1000
        self.moviable = False
        self.stats = stats
    
    def draw(self, ps, game):
        if ps == 1:
            tempPos = worldToScreen(sf.Vector2(self.body.rectangle.left, self.body.rectangle.top))
            self.sprite.position = tempPos
            game.window.draw(self.sprite)
        
    
    def mouseClick(self, game):
        print(self.stats)