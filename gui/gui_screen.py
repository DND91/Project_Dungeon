#!/usr/bin/python
import sfml as sf
import gui.gui_object as gobj

class GuiScreen(gobj.GuiObject):
    def __init__(self, x, y, width, height):
        super().__init__(x,y,width,height)
        self.gui_list = []
        self.bg = sf.RectangleShape()
        self.bg.size = (width, height)
        self.bg.fill_color = sf.Color(131, 139, 131)
        self.bg.outline_color = sf.Color(240, 255, 240)
        self.bg.outline_thickness = 2
        self.bg.position = (x, y)
    
    def update(self, game, delta):
        self.bg.position = (self.rectangle.position.x+game.window.view.center.x-game.window.width/2, self.rectangle.position.y+game.window.view.center.y-game.window.height/2)
        for object in self.gui_list:
            object.update(game, delta)
    
    def drawBackground(self, ps, game):
        game.window.draw(self.bg)
    
    def draw(self, ps, game):
        self.drawBackground(ps, game)
        for object in self.gui_list:
            object.draw(ps, game)
    
    def mouseClick(self, game, screen, rect):
        for object in self.gui_list:
            if object.collision(rect):
                object.mouseClick(game, self, rect)
                self.innerMouseClick(game, object, screen, rect)
                break
        return False
    
    def innerMouseClick(self, game, object, screen, rect):
        x = 0
    
    def keyClick(self, game, code):
        for object in self.gui_list:
            object.keyClick(game, self, code)
        return True