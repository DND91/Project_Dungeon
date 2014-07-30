#!/usr/bin/python
import sfml as sf
from gui.gui_object import *

class GuiText(GuiObject):
    standard_font = 0
    
    def __init__(self, x, y, text):
        super().__init__(x,y, 1, 1)
        self.text = sf.Text(text)
        self.text.character_size = 14
        self.text.color = sf.Color.RED
        self.text.position = self.rectangle.position
        if GuiText.standard_font == 0:
            try:
                GuiText.standard_font = sf.Font.from_file("./resources/arial.ttf")
            except IOError:
                print("No font...")
                raise IOError("Missing font file")
                #exit(1)
        self.text.font = GuiText.standard_font
    
    def collision(self, mouseRect):
        return False
    
    def update(self, game, delta):
        self.text.position = (self.rectangle.position.x+game.window.view.center.x-game.window.width/2, self.rectangle.position.y+game.window.view.center.y-game.window.height/2)
    
    def draw(self, ps, game):
        game.window.draw(self.text)

