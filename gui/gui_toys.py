#!/usr/bin/python
import sfml as sf
from gui.gui_object import *
from math import *

class GuiFollowBall(GuiObject):
    
    def __init__(self, x, y):
        self.rectangle = sf.Rectangle(sf.Vector2(x, y), sf.Vector2(16, 16))
        self.circle = sf.CircleShape(32)
        #self.circle.fill_color = sf.Color.TRANSPARENT
        self.circle.outline_color = sf.Color.RED
        self.circle.outline_thickness = 3
        self.circle.position = (x, y)
        self.speed = 0.5
    
    def update(self, game, delta):
        mousePos = sf.Mouse.get_position(game.window)
        dx = mousePos.x - self.circle.position.x - self.circle.radius
        dy = mousePos.y - self.circle.position.y - self.circle.radius
        distance = sqrt(pow(dx,2) + pow(dy,2))
        if 0.5 < distance :
            rads = atan2(dy,dx)
            rads %= 2*pi
            self.circle.move((cos(rads)*self.speed, sin(rads)*self.speed)) 
    
    def draw(self, ps, game):
        self.circle.texture = game.textures.fetch("HORSE")
        game.window.draw(self.circle)























