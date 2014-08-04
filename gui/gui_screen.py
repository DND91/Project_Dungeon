#!/usr/bin/python
import sfml as sf
import gui.gui_object as gobj

class GuiScreen(gobj.GuiObject):
    def __init__(self, x, y, width, height):
        super().__init__(x,y,width,height)
    
    def update(self, game, delta):
        x = 0
    
    def draw(self, ps, game):
        x = 0
    
    def mouseClick(self, game, screen, rect):
        return False