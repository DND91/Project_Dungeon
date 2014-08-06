#!/usr/bin/python
import sfml as sf
from gui.gui_object import *
import math

class GuiLoadIcon(GuiObject):

    tick = 0
    rotation = 0
    
    def __init__(self, game, x, y):
        super().__init__(x,y, 1, 1)
        txt = game.textures.fetch("LOAD_ICON")
        self.sprite = sf.Sprite(txt)
        self.center = sf.Vector2(txt.width / 2, txt.height / 2)
        self.sprite.origin = self.center
    
    def collision(self, mouseRect):
        return False
    
    def update(self, game, delta):
        self.sprite.position = (self.rectangle.position.x+game.window.view.center.x-game.window.width/2, self.rectangle.position.y+game.window.view.center.y-game.window.height/2)
    
    def draw(self, ps, game):
        GuiLoadIcon.tick += 0.001
        GuiLoadIcon.rotation += 0.1
        self.sprite.rotation = GuiLoadIcon.rotation
        red = math.fabs(math.sin(GuiLoadIcon.tick - 2) * 255)
        green = math.fabs(math.sin(GuiLoadIcon.tick) * 255)
        blue = math.fabs(math.sin(GuiLoadIcon.tick + 2) * 255)
        self.sprite.color = sf.Color(red, green, blue, 255)
        game.window.draw(self.sprite)