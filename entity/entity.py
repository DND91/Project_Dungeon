#!/usr/bin/python
import sfml as sf
from math import *
from world.isometric_tile import *
from world.cool_phys import *
import database.animation_database as vis

class Entity:
    name = "ENTITY"
    anibase = vis.AnimationDatabase()
    
    def __init__(self, animation, world, x, y, width, height):
        self.body = PhysBody(self, x, y, width, height)
        self.rectangle = self.body.rectangle
        self.speed = 0
        self.world = world
        self.moviable = True
        self.solid = True
        self.action = "STILL"
        self.lastAction = self.action
        self.count = 0
        self.animation = animation
        self.visPos = sf.Vector2(0, 0)
    
    def velocity(self, dx, dy):
        self.body.velocity.x = dx
        self.body.velocity.y = dy
    
    def setPosistion(self, pos):
        l, t, w, h = self.body.rectangle
        self.body.rectangle.__init__(pos, (w, h))
    
    def getAngle(self, entity):
        selfPos = self.getCenter()
        entityPos = entity.getCenter()
        dx = entityPos.x - selfPos.x
        dy = entityPos.y - selfPos.y
        rads = atan2(dy,dx)
        rads %= 2*pi
        return rads
    
    def getDistance(self, entity):
        selfPos = self.getCenter()
        entityPos = entity.getCenter()
        dx = entityPos.x - selfPos.x
        dy = entityPos.y - selfPos.y
        distance = sqrt(pow(dx,2) + pow(dy,2))
        return distance
    
    def update(self, game, delta):
        self.rectangle = self.body.rectangle
    
    def draw(self, game):
        self.visPos = worldToScreen(sf.Vector2(self.body.rectangle.left, self.body.rectangle.top))
        self.count += 1
        self.anibase.draw(self.animation, self.action, self.count, self.visPos.x, self.visPos.y, game.window)
    
    def mouseClick(self, game):
        print("BODIES FOUND!")
    
    def getPass(self):
        return 1

class SolidEntity(Entity):
    name = "SOLIDENTITY"
    
    def __init__(self, world, x, y, game):
        super().__init__("SOLID", world, x, y, 64,64)
        self.body.mass = 1000
        self.moviable = False

class BallEntity(Entity):
    name = "BALLENTITY"
    
    def __init__(self, world, x, y, game):
        super().__init__("BALL", world, x, y, 64,64)
        self.body.mass = 2
        self.speed = 0.005
    

class PlayerEntity(Entity):
    name = "PLAYERENTITY"
    
    
    
    def __init__(self, world, x, y, game):
        super().__init__("PLAYER", world, x, y, 64,64)
        self.body.mass = 100
        self.speed = 0.005
    
    
    def update(self, game, delta):
        super().update(game, delta)
        dx = 0
        dy = 0
        self.lastAction = self.action
        next_action = "STILL"
        if sf.Keyboard.is_key_pressed(sf.Keyboard.W):
            #dy += -1
            #dx += -1
            dy -= 1
            next_action = "MOVE"
        if sf.Keyboard.is_key_pressed(sf.Keyboard.S):
            #dy += 1
            #dx += 1
            dy += 1
            next_action = "MOVE"
        if sf.Keyboard.is_key_pressed(sf.Keyboard.D):
            #dy += -1
            #dx += 1
            dx += 1
            next_action = "MOVE"
        if sf.Keyboard.is_key_pressed(sf.Keyboard.A):
            #dy += 1
            #dx += -1
            dx -= 1
            next_action = "MOVE"
        
        self.action = next_action
        if not (self.action == self.lastAction):
            self.count = 0
        
        self.velocity(dx*self.speed, dy*self.speed)
        game.offsetX = self.body.rectangle.left - (game.window.width/2) + (self.body.rectangle.width/2)
        game.offsetY = self.body.rectangle.top - (game.window.height*0.8/2) + (self.body.rectangle.height/2)
        game.window.view.center = worldToScreen(self.body.rectangle.center)
        game.window.view.center = sf.Vector2(game.window.view.center.x+40, game.window.view.center.y+100)
























