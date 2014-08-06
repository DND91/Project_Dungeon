#!/usr/bin/python
import sfml as sf
import gui.gui_object as guio
import gui.gui_text as guit

class GuiProgressBas(guio.GuiObject):
    
    fill_color = sf.Color(240, 255, 240)
    outline_color = sf.Color(131, 139, 131)
    
    activ_outline_color = sf.Color(193, 205, 193)
    activ_fill_color = sf.Color(131, 139, 131)
    
    def __init__(self, x, y, steps = 1000, length = 100):
        super().__init__(x,y, length, 32)
        
        self.currentSteps = 0
        self.goalSteps = steps
        self.endLength = length - 8
        
        self.bg = sf.RectangleShape()
        self.bg.size = (length, 32)
        self.bg.fill_color = self.fill_color
        self.bg.outline_color = self.outline_color
        self.bg.outline_thickness = 4
        self.bg.position = (x, y)
        
        self.bar = sf.RectangleShape()
        self.bar.size = (0, 32 - 8)
        self.bar.fill_color = sf.Color.BLUE
        self.bar.outline_thickness = 0
        self.bar.position = (x + 4, y + 4)
        
        self.text = guit.GuiText(x + 16, y + 6, "Loading...")
    
    def update(self, game, delta):
        self.text.update(game, delta)
        pos = (self.rectangle.position.x+game.window.view.center.x-game.window.width/2, self.rectangle.position.y+game.window.view.center.y-game.window.height/2)
        self.bg.position = pos
        self.bar.position = (pos[0]+4, pos[1]+4)
        
        if self.currentSteps <= self.goalSteps:
            m = self.currentSteps / self.goalSteps
            self.bar.size = (m * self.endLength, 32 - 8)
        
        
        
    
    def draw(self, ps, game):
        game.window.draw(self.bg)
        game.window.draw(self.bar)
        self.text.draw(ps, game)
    
    
    
    