#!/usr/bin/python
import sfml as sf
from gui.gui_object import *
from gui.gui_text import *

class GuiButton(GuiObject):
    outline_color = sf.Color(131, 139, 131)
    activ_outline_color = sf.Color(193, 205, 193)
    fill_color = sf.Color(240, 255, 240)
    activ_fill_color = sf.Color(131, 139, 131)
    
    def __init__(self, x,y, text):
        super().__init__(x,y, len(text)*8+12, 18)
        self.text = GuiText(x+3,y+1, text)
        self.bg = sf.RectangleShape()
        self.bg.size = (len(text)*8+10, 18)
        self.bg.fill_color = self.fill_color
        self.bg.outline_color = self.outline_color
        self.bg.outline_thickness = 2
        self.bg.position = (x, y)
    
    def update(self, game, delta):
        self.text.update(game, delta)
        self.bg.position = (self.rectangle.position.x+game.window.view.center.x-game.window.width/2, self.rectangle.position.y+game.window.view.center.y-game.window.height/2)
        mousePressed = sf.Mouse.is_button_pressed(sf.Mouse.LEFT)
        collided = self.collision(sf.Rectangle(sf.Mouse.get_position(game.window), sf.Vector2(4, 4)))
        if mousePressed and collided:
            self.bg.fill_color = self.activ_fill_color
            self.bg.outline_color = self.activ_outline_color
        else:
            self.bg.fill_color = self.fill_color
            self.bg.outline_color = self.outline_color
    
    def draw(self, ps, game):
        game.window.draw(self.bg)
        self.text.draw(ps, game)